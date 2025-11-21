<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController;

/*
|--------------------------------------------------------------------------
| API Routes - AUTH SERVICE
|--------------------------------------------------------------------------
*/

// 1. RUTA PÚBLICA (Sin seguridad, para el Health Check del Gateway)
Route::get('/health', function () {
    return response()->json([
        'status' => 'healthy',
        'service' => 'auth-service',
        'timestamp' => now()->toISOString(),
        'database' => 'connected'
    ], 200);
});

// 2. RUTAS PROTEGIDAS POR EL GATEWAY
// Todas estas rutas requieren el header 'X-API-Key' que inyecta el Gateway
Route::middleware('gateway.auth')->group(function () {

    // --- Autenticación Pública (Login/Registro) ---
    // Aunque son públicas para el usuario, para el microservicio son internas
    // y deben venir firmadas por el Gateway.
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
    Route::post('/reset-password', [AuthController::class, 'resetPassword']);

    // --- Rutas Protegidas por Token (Sanctum) ---
    Route::middleware('auth:sanctum')->group(function () {
        Route::post('/logout', [AuthController::class, 'logout']);
        Route::get('/me', [AuthController::class, 'me']);
        Route::get('/user', function (Request $request) {
            return $request->user();
        });
    });

    // --- Rutas de Administrador ---
    Route::middleware(['auth:sanctum', 'role:admin'])->group(function () {
        Route::get('/usuarios', [UserController::class, 'index']);           
        Route::get('/usuarios/{id}', [UserController::class, 'show']);       
        Route::put('/usuarios/{id}', [UserController::class, 'update']);     
        Route::delete('/usuarios/{id}', [UserController::class, 'destroy']); 
        Route::post('/usuarios/buscar', [UserController::class, 'search']);  
        Route::get('/usuarios/stats', [UserController::class, 'stats']);     
    });

    // --- Rutas de Usuario Regular ---
    Route::middleware(['auth:sanctum', 'role:usuario'])->group(function () {
        Route::get('/usuarios/stats', [UserController::class, 'stats']);
    });

});