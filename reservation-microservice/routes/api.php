<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ReservaController;

/*
|--------------------------------------------------------------------------
| API Routes - RESERVATION SERVICE
|--------------------------------------------------------------------------
*/

// 1. RUTA PÚBLICA (Sin seguridad, para el Health Check del Gateway)
Route::get('/health', function () {
    return response()->json([
        'status' => 'healthy',
        'service' => 'reservation-service',
        'timestamp' => now()->toISOString()
    ], 200);
});

// 2. RUTAS PROTEGIDAS POR EL GATEWAY
// Requieren que la petición venga del Gateway con la API Key correcta
Route::middleware('gateway.auth')->group(function () {

    // Test de usuario (si se requiere validar token Sanctum aquí también)
    Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
        return $request->user();
    });

    // CRUD de Reservas
    Route::apiResource('reservas', ReservaController::class);

    // Rutas adicionales de estado
    Route::put('reservas/{id}/confirmar', [ReservaController::class, 'confirmar']);
    Route::put('reservas/{id}/cancelar', [ReservaController::class, 'cancelar']);

});