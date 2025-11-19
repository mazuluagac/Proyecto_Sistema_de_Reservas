<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Middleware to validate incoming requests contain a valid gateway API key.
 *
 * Checks the header `X-Gateway-Api-Key` (falls back to `Gateway-Api-Key` or `x-api-key`) and
 * compares it to the value of the environment variable `GATEWAY_API_KEY`.
 * If missing or invalid, returns a 401 JSON response.
 */
class ValidateGatewayApiKey
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle(Request $request, Closure $next)
    {
        // Try common header names (including the simpler X-API-KEY)
        $headerKey = $request->header('X-Gateway-Api-Key')
            ?: $request->header('Gateway-Api-Key')
            ?: $request->header('X-API-KEY')
            ?: $request->header('x-api-key');

        // Expected key comes from env or config (prefer GATEWAY_API_KEY, accept API_KEY for compatibility)
        $expected = env('GATEWAY_API_KEY') ?: env('API_KEY') ?: config('app.gateway_api_key') ?: null;

        // If no expected key configured, deny access (safer than allowing through)
        if (empty($expected) || empty($headerKey) || !is_string($headerKey)) {
            return response()->json(['message' => 'Unauthorized: missing gateway API key'], Response::HTTP_UNAUTHORIZED);
        }

        // Use hash_equals to avoid timing attacks
        if (!hash_equals((string) $expected, (string) $headerKey)) {
            return response()->json(['message' => 'Unauthorized: invalid gateway API key'], Response::HTTP_UNAUTHORIZED);
        }

        return $next($request);
    }
}