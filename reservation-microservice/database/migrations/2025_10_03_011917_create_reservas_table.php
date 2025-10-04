<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateReservasTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('reservas', function (Blueprint $table) {
            $table->id(); // ID de la reserva
            $table->unsignedBigInteger('usuario_id'); // ID del usuario que hace la reserva
            $table->string('nombre_usuario', 100); // Nombre de quien reserva
            $table->date('fecha_inicio');
            $table->date('fecha_fin');
            $table->string('descripcion', 255)->nullable(); // Breve descripción
            $table->enum('estado', ['pendiente', 'confirmada', 'cancelada'])->default('pendiente');
            $table->timestamps();
            
            // Índices básicos para mejorar consultas
            $table->index('usuario_id');
            $table->index('fecha_inicio');
            $table->index('estado');
        });
    }


    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('reservas');
    }
}
