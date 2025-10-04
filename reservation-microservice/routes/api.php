<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ReservaController;

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

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

// Rutas para Reservas
Route::apiResource('reservas', ReservaController::class);

// Rutas adicionales para gestión de estado
Route::put('reservas/{id}/confirmar', [ReservaController::class, 'confirmar']);
Route::put('reservas/{id}/cancelar', [ReservaController::class, 'cancelar']);
