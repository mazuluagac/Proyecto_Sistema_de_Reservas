<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;

class GatewayController extends Controller
{
    protected $services = [];
    protected $apiKey;

    public function __construct()
    {
        #estos valores pueden ser configurados en el archivo .env
        $this->services = [
            #estos son los URLs base de los microservicios
            'auth' => env('AUTH_SERVICE_URL', env('MICROSERVICE_API_URL')),
            'reservation' => env('RESERVATION_SERVICE_URL'),
            'reports' => env('REPORTS_SERVICE_URL'),
            'notifications' => env('NOTIFICATIONS_SERVICE_URL'),
            'audit' => env('AUDIT_SERVICE_URL'),
            'default' => env('MICROSERVICE_API_URL'),
        ];
        $this->apiKey = env('API_KEY');
    }

    protected function getServiceBaseUrl(string $service = null)
    {
        if (!$service) {
            return $this->services['default'] ?? null;
        }
        return $this->services[$service] ?? $this->services['default'] ?? null;
    }

    /**
     * Proxy genérico: reenvía cualquier petición al microservicio indicado.
     * Ruta sugerida: /gateway/{service}/{endpoint?}
     */
    public function proxy(Request $request, string $service, string $endpoint = '')
    {
        $base = $this->getServiceBaseUrl($service);
        if (!$base) {
            return response()->json(['error' => 'Servicio desconocido: ' . $service], 404);
        }

        $path = ltrim($endpoint, '/');
        $query = $request->getQueryString();
        $url = rtrim($base, '/') . ($path !== '' ? '/' . $path : '') . ($query ? '?' . $query : '');

        $method = strtoupper($request->method());

        // Construir headers a reenviar
        //funciona para el API-KEY permitiendo la autenticación entre microservicios
        $headers = [
            'X-API-KEY' => $this->apiKey,
        ];
        if ($auth = $request->header('Authorization')) {
            $headers['Authorization'] = $auth;
        }
        foreach (['Accept', 'Content-Type'] as $h) {
            if ($v = $request->header($h)) {
                $headers[$h] = $v;
            }
        }

        try {
            $pending = Http::withHeaders($headers)->withOptions(['timeout' => 30]);

            // Si hay archivos, usar multipart
            $files = $request->files->all();
            if (!empty($files) && in_array($method, ['POST', 'PUT', 'PATCH'])) {
                $pending = $pending->asMultipart();
                foreach ($files as $key => $file) {
                    if (is_array($file)) {
                        foreach ($file as $f) {
                            $pending = $pending->attach($key, fopen($f->getRealPath(), 'r'), $f->getClientOriginalName());
                        }
                    } else {
                        $pending = $pending->attach($key, fopen($file->getRealPath(), 'r'), $file->getClientOriginalName());
                    }
                }
                $fields = $request->except(array_keys($files));
                switch ($method) {
                    case 'POST':
                        $response = $pending->post($url, $fields);
                        break;
                    case 'PUT':
                        $response = $pending->put($url, $fields);
                        break;
                    case 'PATCH':
                        $response = $pending->patch($url, $fields);
                        break;
                    default:
                        $response = $pending->send($method, $url);
                }
            } else {
                switch ($method) {
                    case 'GET':
                        $response = Cache::remember("gateway:$url", 10, function() use ($pending, $url) {
                            return $pending->get($url);
                        });
                        break;
                    case 'POST':
                        if ($request->header('Content-Type') && strpos($request->header('Content-Type'), 'application/x-www-form-urlencoded') !== false) {
                            $response = $pending->asForm()->post($url, $request->all());
                        } else {
                            $response = $pending->post($url, $request->all());
                        }
                        break;
                    case 'PUT':
                        $response = $pending->put($url, $request->all());
                        break;
                    case 'PATCH':
                        $response = $pending->patch($url, $request->all());
                        break;
                    case 'DELETE':
                        $response = $pending->delete($url);
                        break;
                    default:
                        $response = $pending->send($method, $url);
                }
            }
        } catch (\Exception $e) {
            return response()->json(['error' => 'Error de conexión al servicio', 'message' => $e->getMessage()], 502);
        }

        $resHeaders = [];
        foreach ($response->headers() as $k => $v) {
            $resHeaders[$k] = is_array($v) ? implode(';', $v) : $v;
        }

        return response($response->body(), $response->status())->withHeaders($resHeaders);
    }

    // Métodos de conveniencia que delegan al proxy
    public function index(Request $request, string $service, string $any = '')
    {
        return $this->proxy($request, $service, $any);
    }

    public function store(Request $request, string $service, string $any = '')
    {
        return $this->proxy($request, $service, $any);
    }

    public function show(Request $request, string $service, string $any = '')
    {
        return $this->proxy($request, $service, $any);
    }

    public function update(Request $request, string $service, string $any = '')
    {
        return $this->proxy($request, $service, $any);
    }

    public function destroy(Request $request, string $service, string $any = '')
    {
        return $this->proxy($request, $service, $any);
    }
}
