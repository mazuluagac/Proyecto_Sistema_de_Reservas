<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

// Public auth routes
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
Route::post('/reset-password', [AuthController::class, 'resetPassword']);

// Protected auth routes
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me', [AuthController::class, 'me']);
    Route::get('/user', function (Request $request) {
        return $request->user();
    });
});

// Admin only routes
Route::middleware(['auth:sanctum', 'role:admin'])->group(function () {
    // Gestión completa de usuarios (solo administradores)
    Route::get('/usuarios', [UserController::class, 'index']);           // Listar usuarios
    Route::get('/usuarios/{id}', [UserController::class, 'show']);       // Obtener usuario por ID
    Route::put('/usuarios/{id}', [UserController::class, 'update']);     // Actualizar usuario
    Route::delete('/usuarios/{id}', [UserController::class, 'destroy']); // Eliminar usuario
    Route::post('/usuarios/buscar', [UserController::class, 'search']);  // Buscar usuarios
    Route::get('/usuarios/stats', [UserController::class, 'stats']);     // Estadísticas de usuarios
});

// User only routes  
Route::middleware(['auth:sanctum', 'role:usuario'])->group(function () {
    // Los usuarios regulares solo pueden ver estadísticas básicas
    Route::get('/usuarios/stats', [UserController::class, 'stats']);
});
