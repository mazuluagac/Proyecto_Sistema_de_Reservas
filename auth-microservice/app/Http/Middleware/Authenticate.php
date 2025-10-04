<?php

namespace App\Http\Middleware;

use Illuminate\Auth\Middleware\Authenticate as Middleware;

class Authenticate extends Middleware
{
    /**
     * Get the path the user should be redirected to when they are not authenticated.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return string|null
     */
    protected function redirectTo($request)
    {
        // Para APIs, no redirigir sino retornar null para que Laravel 
        // maneje la respuesta como error 401 JSON
        if (! $request->expectsJson()) {
            return null; // Cambiado de route('login') a null
        }
    }
}
