<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// Ruta pública para el Health Check del Gateway
Route::get('/health', function () {
    return response()->json([
        'status' => 'healthy',
        'service' => 'Auth Service'
    ]);
});

Route::get('/', function () {
    return view('welcome');
});
