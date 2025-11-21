<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class ValidateGatewayKey
{
    public function handle(Request $request, Closure $next)
    {
        // Obtenemos la llave del entorno (inyectada por Docker)
        $validKey = env('API_KEY');
        
        // Obtenemos la llave que envía la petición
        $requestKey = $request->header('X-API-Key');

        // Si no coinciden, rechazamos (401 Unauthorized)
        if ($requestKey !== $validKey) {
            return response()->json([
                'error' => 'Acceso denegado',
                'message' => 'Petición no autorizada por el API Gateway'
            ], 401);
        }

        return $next($request);
    }
}