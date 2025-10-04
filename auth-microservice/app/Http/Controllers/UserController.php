<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;

class UserController extends Controller
{
    /**
     * Listar todos los usuarios con paginación
     */
    public function index(Request $request): JsonResponse
    {
        try {
            // Obtener parámetros de paginación
            $page = $request->get('page', 1);
            $limit = $request->get('limit', 10);
            
            // Validar límite
            if ($limit > 100) $limit = 100;
            if ($limit < 1) $limit = 10;

            // Obtener usuarios con paginación
            $usuarios = User::select('id', 'name', 'email', 'role', 'created_at', 'updated_at')
                          ->paginate($limit, ['*'], 'page', $page);

            return response()->json([
                'success' => true,
                'message' => 'Usuarios obtenidos exitosamente',
                'data' => [
                    'usuarios' => $usuarios->items(),
                    'pagination' => [
                        'page' => $usuarios->currentPage(),
                        'limit' => $usuarios->perPage(),
                        'total' => $usuarios->total(),
                        'pages' => $usuarios->lastPage()
                    ]
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error obteniendo usuarios: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Obtener un usuario por ID
     */
    public function show($id): JsonResponse
    {
        try {
            $usuario = User::select('id', 'name', 'email', 'role', 'created_at', 'updated_at')
                          ->find($id);

            if (!$usuario) {
                return response()->json([
                    'success' => false,
                    'message' => 'Usuario no encontrado'
                ], 404);
            }

            return response()->json([
                'success' => true,
                'message' => 'Usuario obtenido exitosamente',
                'data' => [
                    'usuario' => $usuario
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error obteniendo usuario: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Actualizar un usuario existente
     */
    public function update(Request $request, $id): JsonResponse
    {
        try {
            // Verificar que el usuario existe
            $usuario = User::find($id);
            if (!$usuario) {
                return response()->json([
                    'success' => false,
                    'message' => 'Usuario no encontrado'
                ], 404);
            }

            // Validar datos de entrada
            $validator = Validator::make($request->all(), [
                'name' => 'sometimes|string|max:255',
                'email' => 'sometimes|string|email|max:255|unique:users,email,' . $id,
                'password' => 'sometimes|string|min:8',
                'role' => 'sometimes|in:admin,usuario'
            ]);

            if ($validator->fails()) {
                return response()->json([
                    'success' => false,
                    'message' => 'Errores de validación',
                    'errors' => $validator->errors()
                ], 422);
            }

            // Actualizar solo los campos proporcionados
            $datosActualizacion = [];
            
            if ($request->has('name')) {
                $datosActualizacion['name'] = $request->name;
            }
            
            if ($request->has('email')) {
                $datosActualizacion['email'] = $request->email;
            }
            
            if ($request->has('password')) {
                $datosActualizacion['password'] = Hash::make($request->password);
            }
            
            if ($request->has('role')) {
                $datosActualizacion['role'] = $request->role;
            }

            // Actualizar usuario
            $usuario->update($datosActualizacion);

            // Retornar usuario actualizado
            $usuarioActualizado = User::select('id', 'name', 'email', 'role', 'created_at', 'updated_at')
                                    ->find($id);

            return response()->json([
                'success' => true,
                'message' => 'Usuario actualizado exitosamente',
                'data' => [
                    'usuario' => $usuarioActualizado
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error actualizando usuario: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Eliminar un usuario
     */
    public function destroy($id): JsonResponse
    {
        try {
            $usuario = User::find($id);
            
            if (!$usuario) {
                return response()->json([
                    'success' => false,
                    'message' => 'Usuario no encontrado'
                ], 404);
            }

            // Eliminar usuario
            $usuario->delete();

            return response()->json([
                'success' => true,
                'message' => 'Usuario eliminado exitosamente',
                'data' => [
                    'user_id' => $id
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error eliminando usuario: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Buscar usuarios por nombre o email
     */
    public function search(Request $request): JsonResponse
    {
        try {
            $validator = Validator::make($request->all(), [
                'buscar' => 'required|string|min:1'
            ]);

            if ($validator->fails()) {
                return response()->json([
                    'success' => false,
                    'message' => 'Debe proporcionar un término de búsqueda',
                    'errors' => $validator->errors()
                ], 422);
            }

            $terminoBusqueda = $request->buscar;
            $page = $request->get('page', 1);
            $limit = $request->get('limit', 10);

            // Buscar usuarios que contengan el término en nombre o email
            $usuarios = User::select('id', 'name', 'email', 'role', 'created_at', 'updated_at')
                          ->where('name', 'LIKE', '%' . $terminoBusqueda . '%')
                          ->orWhere('email', 'LIKE', '%' . $terminoBusqueda . '%')
                          ->paginate($limit, ['*'], 'page', $page);

            return response()->json([
                'success' => true,
                'message' => 'Búsqueda realizada exitosamente',
                'data' => [
                    'usuarios' => $usuarios->items(),
                    'pagination' => [
                        'page' => $usuarios->currentPage(),
                        'limit' => $usuarios->perPage(),
                        'total' => $usuarios->total(),
                        'pages' => $usuarios->lastPage()
                    ],
                    'busqueda' => $terminoBusqueda
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error en la búsqueda: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Obtener estadísticas de usuarios
     */
    public function stats(): JsonResponse
    {
        try {
            $totalUsuarios = User::count();
            $totalAdmins = User::where('role', 'admin')->count();
            $totalUsuariosRegulares = User::where('role', 'usuario')->count();

            return response()->json([
                'success' => true,
                'message' => 'Estadísticas obtenidas exitosamente',
                'data' => [
                    'stats' => [
                        'total_usuarios' => $totalUsuarios,
                        'total_admins' => $totalAdmins,
                        'total_usuarios_regulares' => $totalUsuariosRegulares,
                        'servicio' => 'Auth Microservice - Gestión de Usuarios',
                        'base_datos' => 'MySQL/PostgreSQL'
                    ]
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error obteniendo estadísticas: ' . $e->getMessage()
            ], 500);
        }
    }
}