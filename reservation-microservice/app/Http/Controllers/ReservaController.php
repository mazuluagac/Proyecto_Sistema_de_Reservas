<?php

namespace App\Http\Controllers;

use App\Models\Reserva;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class ReservaController extends Controller
{
    /**
     * Obtener todas las reservas
     */
    public function index(): JsonResponse
    {
        $reservas = Reserva::orderBy('fecha_inicio')->get();
        
        return response()->json([
            'success' => true,
            'data' => $reservas
        ]);
    }

    /**
     * Crear una nueva reserva
     */
    public function store(Request $request): JsonResponse
    {
        $request->validate([
            'usuario_id' => 'required|integer',
            'nombre_usuario' => 'required|string|max:100',
            'fecha_inicio' => 'required|date|date_format:Y-m-d',
            'fecha_fin' => 'required|date|date_format:Y-m-d|after_or_equal:fecha_inicio',
            'descripcion' => 'nullable|string|max:255',
            'estado' => 'nullable|in:pendiente,confirmada,cancelada'
        ]);

        $reserva = Reserva::create([
            'usuario_id' => $request->usuario_id,
            'nombre_usuario' => $request->nombre_usuario,
            'fecha_inicio' => $request->fecha_inicio,
            'fecha_fin' => $request->fecha_fin,
            'descripcion' => $request->descripcion,
            'estado' => $request->estado ?? 'pendiente'
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Reserva creada exitosamente',
            'data' => $reserva
        ], 201);
    }

    /**
     * Mostrar una reserva específica
     */
    public function show($id): JsonResponse
    {
        $reserva = Reserva::find($id);

        if (!$reserva) {
            return response()->json([
                'success' => false,
                'message' => 'Reserva no encontrada'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'data' => $reserva
        ]);
    }

    /**
     * Actualizar una reserva
     */
    public function update(Request $request, $id): JsonResponse
    {
        $reserva = Reserva::find($id);

        if (!$reserva) {
            return response()->json([
                'success' => false,
                'message' => 'Reserva no encontrada'
            ], 404);
        }

        $request->validate([
            'usuario_id' => 'sometimes|integer',
            'nombre_usuario' => 'sometimes|string|max:100',
            'fecha_inicio' => 'sometimes|date|date_format:Y-m-d',
            'fecha_fin' => 'sometimes|date|date_format:Y-m-d|after_or_equal:fecha_inicio',
            'descripcion' => 'nullable|string|max:255',
            'estado' => 'sometimes|in:pendiente,confirmada,cancelada'
        ]);

        $reserva->update($request->only([
            'usuario_id', 'nombre_usuario', 'fecha_inicio', 
            'fecha_fin', 'descripcion', 'estado'
        ]));

        return response()->json([
            'success' => true,
            'message' => 'Reserva actualizada exitosamente',
            'data' => $reserva
        ]);
    }

    /**
     * Eliminar una reserva
     */
    public function destroy($id): JsonResponse
    {
        $reserva = Reserva::find($id);

        if (!$reserva) {
            return response()->json([
                'success' => false,
                'message' => 'Reserva no encontrada'
            ], 404);
        }

        $reserva->delete();

        return response()->json([
            'success' => true,
            'message' => 'Reserva eliminada exitosamente'
        ]);
    }

    /**
     * Confirmar una reserva
     */
    public function confirmar($id): JsonResponse
    {
        $reserva = Reserva::find($id);

        if (!$reserva) {
            return response()->json([
                'success' => false,
                'message' => 'Reserva no encontrada'
            ], 404);
        }

        $reserva->update(['estado' => 'confirmada']);

        return response()->json([
            'success' => true,
            'message' => 'Reserva confirmada exitosamente',
            'data' => $reserva
        ]);
    }

    /**
     * Cancelar una reserva
     */
    public function cancelar($id): JsonResponse
    {
        $reserva = Reserva::find($id);

        if (!$reserva) {
            return response()->json([
                'success' => false,
                'message' => 'Reserva no encontrada'
            ], 404);
        }

        $reserva->update(['estado' => 'cancelada']);

        return response()->json([
            'success' => true,
            'message' => 'Reserva cancelada exitosamente',
            'data' => $reserva
        ]);
    }
}