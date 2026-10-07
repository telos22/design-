"""책상 위 소품: A4 종이, 펼친 노트, 펜. 단위 1 = 10cm. (x, y)는 판 위 위치, z는 판 윗면 높이."""
import math

import bpy

import studio

_mats = {}


def _mat(name, *args, **kw):
    if name not in _mats or _mats[name].name not in bpy.data.materials:
        _mats[name] = studio.material(name, *args, **kw)
    return _mats[name]


def paper(x, y, z, angle=0.0):
    """A4 21 × 29.7cm"""
    s = studio.box("A4", (2.1, 2.97, 0.006), (x, y, z + 0.003), _mat("Paper", (0.8, 0.8, 0.78), roughness=0.9))
    s.rotation_euler.z = angle
    return s


def notebook(x, y, z, angle=0.0):
    """펼친 A5 노트: 표지 + 양쪽 페이지 묶음 + 가운데 접힌 선"""
    parts = [studio.box("NoteCover", (3.04, 2.14, 0.03), (x, y, z + 0.015),
                        _mat("Cover", (0.05, 0.05, 0.055), roughness=0.7), bevel=0.01)]
    page = _mat("Pages", (0.78, 0.76, 0.70), roughness=0.95)
    for sx in (-1, 1):
        parts.append(studio.box("NotePages", (1.46, 2.06, 0.06), (x + sx * 0.75, y, z + 0.06), page, bevel=0.01))
    for i in range(10):  # 줄 노트의 줄
        for sx in (-1, 1):
            parts.append(studio.box("Line", (1.2, 0.006, 0.002), (x + sx * 0.75, y - 0.8 + i * 0.18, z + 0.091),
                                    _mat("Ruling", (0.45, 0.5, 0.6), roughness=0.9)))
    parts.append(studio.box("Gutter", (0.02, 2.06, 0.002), (x, y, z + 0.091), _mat("Shade", (0.3, 0.3, 0.3))))
    for p in parts:   # 노트 전체를 (x, y) 중심으로 회전
        dx, dy = p.location.x - x, p.location.y - y
        c, s = math.cos(angle), math.sin(angle)
        p.location.x, p.location.y = x + dx * c - dy * s, y + dx * s + dy * c
        p.rotation_euler.z = angle
    return parts


def pen(x, y, z, angle=0.0):
    """지름 1cm, 길이 14cm 펜"""
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.05, depth=1.4, location=(x, y, z + 0.05))
    body = bpy.context.object
    body.rotation_euler = (0, math.pi / 2, angle)
    studio.assign(body, _mat("PenBody", (0.03, 0.03, 0.035), roughness=0.3, metallic=0.4))
    bpy.ops.object.shade_smooth()
    return body


def desk_set(x, y, z):
    """비교용 기본 배치: 왼쪽 펼친 노트, 오른쪽 A4, 그 위 펜"""
    notebook(x - 1.9, y - 0.6, z, angle=0.05)
    paper(x + 1.9, y + 0.3, z, angle=-0.12)
    pen(x + 2.0, y - 0.3, z + 0.006, angle=0.6)
