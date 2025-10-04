<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Validator;

class AuthController extends Controller
{
    /**
     * Register a new user
     */
    public function register(Request $request): JsonResponse
    {
        //su funcion es validar y crear un nuevo usuario
        $validator = Validator::make($request->all(), [
            //su estructura es:
            //name, email, password, role
            //required: obligatorio
            //sometimes: opcional
            'name' => 'required|string|max:255',
            //unique:users -> el email debe ser unico en la tabla users
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
            'role' => 'sometimes|in:admin,usuario'
        ]);

        //si la validacion falla, retorna errores
        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation errors',
                'errors' => $validator->errors()
            ], 422);
            /**422: ocurre cuando un servidor recibe una solicitud que, aunque 
             * sintácticamente correcta, contiene datos o errores semánticos 
             * que impiden su procesamiento */
        }

        // Crear el usuario
        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
            'role' => $request->role ?? 'usuario'
        ]);

        // Crear token de autenticación para el usuario 
        $token = $user->createToken('auth_token')->plainTextToken;

        // Retornar respuesta
        return response()->json([
            'success' => true,
            'message' => 'User registered successfully',
            'data' => [
                'user' => [
                    'id' => $user->id,
                    'name' => $user->name,
                    'email' => $user->email,
                    'role' => $user->role
                ],
                'token' => $token
            ]
        ], 201);
    }

    /**
     * Login user
     */
    public function login(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'email' => 'required|email',
            'password' => 'required'
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation errors',
                'errors' => $validator->errors()
            ], 422);
        }

        //en esta parte se autentica al usuario
        //si la autenticacion falla, retorna un error
        if (!Auth::attempt($request->only('email', 'password'))) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid credentials'
            ], 401);
        }

        // Si la autenticación es exitosa, obtener el usuario y crear un token
        $user = User::where('email', $request->email)->firstOrFail();
        //el metodo createToken es proporcionado por Laravel Sanctum
        //y genera un token de acceso para el usuario autenticado
        $token = $user->createToken('auth_token')->plainTextToken;

        // Retornar respuesta
        return response()->json([
            'success' => true,
            'message' => 'Login successful',
            'data' => [
                'user' => [
                    'id' => $user->id,
                    'name' => $user->name,
                    'email' => $user->email,
                    'role' => $user->role
                ],
                //el token de acceso luego puede ser usado para autenticar
                //las solicitudes a rutas protegidas
                'token' => $token
            ]
        ]);
    }

    /**
     * Logout user
     */
    public function logout(Request $request): JsonResponse
    {
        //elimina el token de acceso actual del usuario autenticado
        //lo que efectivamente cierra la sesion
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'success' => true,
            'message' => 'Logged out successfully'
        ]);
    }

    /**
     * Get authenticated user
     */
    //me: devuelve los detalles del usuario autenticado
    //como id, name, email, role
    public function me(Request $request): JsonResponse
    {
        $user = $request->user();

        return response()->json([
            'success' => true,
            'data' => [
                'user' => [
                    'id' => $user->id,
                    'name' => $user->name,
                    'email' => $user->email,
                    'role' => $user->role
                ]
            ]
        ]);
    }

    /**
     * Send password reset link
     */
    public function forgotPassword(Request $request): JsonResponse
    {
        //validar que el email es correcto y existe en la base de datos
        $validator = Validator::make($request->all(), [
            'email' => 'required|email|exists:users'
        ]);

        //verificar si hay errores de validacion
        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation errors',
                'errors' => $validator->errors()
            ], 422);
        }

        //enviar el enlace de restablecimiento de contraseña
        $status = Password::sendResetLink(
            $request->only('email')
        );

        //verificar si el enlace fue enviado exitosamente
        if ($status === Password::RESET_LINK_SENT) {
            return response()->json([
                'success' => true,
                'message' => 'Password reset link sent to your email'
            ]);
        }

        //si hubo un error al enviar el enlace
        return response()->json([
            'success' => false,
            'message' => 'Unable to send reset link'
        ], 500);
    }

    /**
     * Reset password
     */
    //resetPassword: permite a un usuario restablecer su contraseña
    //usando un token de restablecimiento enviado por correo
    public function resetPassword(Request $request): JsonResponse
    {
        //validar token, email, nueva contraseña y confirmación
        //si hay errores, retornar mensajes de error
        $validator = Validator::make($request->all(), [
            'token' => 'required',
            'email' => 'required|email',
            'password' => 'required|string|min:8|confirmed'
        ]);
        
        //verificar si hay errores de validacion
        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'message' => 'Validation errors',
                'errors' => $validator->errors()
            ], 422);
        }

        //intentar restablecer la contraseña
        //si el token y email son validos, actualizar la contraseña
        $status = Password::reset(
            $request->only('email', 'password', 'password_confirmation', 'token'),
            function ($user, $password) {
                //actualizar la contraseña del usuario
                //usando Hash::make para encriptarla
                $user->forceFill([
                    'password' => Hash::make($password)
                ])->save();
            }
        );

        //verificar el estado del restablecimiento
        if ($status === Password::PASSWORD_RESET) {
            return response()->json([
                'success' => true,
                'message' => 'Password reset successfully'
            ]);
        }

        return response()->json([
            'success' => false,
            'message' => 'Invalid token or email'
        ], 400);
    }
}