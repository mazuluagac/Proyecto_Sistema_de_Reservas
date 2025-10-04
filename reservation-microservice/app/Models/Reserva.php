<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Reserva extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'usuario_id',
        'nombre_usuario',
        'fecha_inicio',
        'fecha_fin',
        'descripcion',
        'estado',
    ];

    /**
     * The attributes that should be cast.
     */
    protected $casts = [
        'fecha_inicio' => 'date',
        'fecha_fin' => 'date',
    ];
}
