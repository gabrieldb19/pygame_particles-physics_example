from particle import Particle
import pygame as pg


def bounds_collision(p: Particle, w: int, h: int) -> None:
    """ Calculo del rebote en los bordes del entorno.

    Args:
        p (Particle): Particula xD
        w (int): width(ancho) del entorno.
        h (int): height(alto) del entorno.
    """
    if p.position.x <= 0 + p.size:
        p.position.x = 0 + p.size
        p.vx = -p.vx * p.restitution
        if abs(p.vx) < 0.01:
            p.vx = 0
    if p.position.x >= w - p.size:
        p.position.x = w - p.size
        p.vx = -p.vx * p.restitution
        if abs(p.vx) < -0.01:
            p.vx = 0
    if p.position.y <= 0 + p.size:
        p.position.y = 0 + p.size
        p.vy = -p.vy * p.restitution
        if abs(p.vy) < 0.01:
            p.vy = 0
    if p.position.y >= h - p.size:
        p.position.y = h - p.size
        p.vy = -p.vy * p.restitution
        if abs(p.vy) < -0.01:
            p.vy = 0

def check_collision(p1: Particle, p2: Particle) -> bool:
    """ Verifica si dos particulas estan colisionando.

    Args:
        p1 (Particle): Particula 1
        p2 (Particle): Particula 2

    Returns:
        bool: Creo que se explica solo xD
    """
    distance = p1.position.distance_to(p2.position)
    return distance <= p1.size + p2.size

def resolve_collision(p1: Particle, p2: Particle) -> None:
    """ Calcula la correccion en las velocidades al colisionar dos particulas.

    Args:
        p1 (Particle): Particula 1.
        p2 (Particle): Particula 2.
    """
    # Obtener el vector de colisión
    collision_vector = p1.position - p2.position
    collision_vector = collision_vector.normalize()

    # Obtener la velocidad relativa de las partículas en la dirección de la colisión
    relative_velocity = pg.math.Vector2(p1.vx - p2.vx, p1.vy - p2.vy)
    speed_along_collision = relative_velocity.dot(collision_vector)

    # Si las partículas ya están separándose, no hacemos nada
    if speed_along_collision > 0:
        return

    # Usar coeficiente de restitución para calcular el impulso
    restitution = min(p1.restitution, p2.restitution)

    # Impulso escalar
    impulse = (-(1 + restitution) * speed_along_collision) / (1/p1.mass + 1/p2.mass)

    # Aplicar el impulso a cada partícula
    impulse_vector = impulse * collision_vector
    p1.vx += impulse_vector.x / p1.mass
    p1.vy += impulse_vector.y / p1.mass
    p2.vx -= impulse_vector.x / p2.mass
    p2.vy -= impulse_vector.y / p2.mass