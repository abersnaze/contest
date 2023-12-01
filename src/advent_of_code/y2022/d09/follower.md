Comparison of various follower functions.

in rust by Robin Tonen
```
fn follow((hx, hy): (i64, i64), (tx, ty): (i64, i64)) -> (i64, i64) {
    let (dx, dy) = (hx - tx, hy - ty);
    let nx = match (dx, dy) {
        (2, _) => tx + 1,
        (-2, _) => tx - 1,
        (_, y) if y.abs() == 2 => hx,
        _ => tx,
    };
    let ny = match (dx, dy) {
        (_, 2) => ty + 1,
        (_, -2) => ty - 1,
        (x, _) if x.abs() == 2 => hy,
        _ => ty,
    };
    (nx, ny)
}
```

in python by George Campbell
```
def follow(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    mx = abs(dx)  # magnitude 
    my = abs(dy)
    dx = sign(dx) # sign
    dy = sign(dy)
    if math.sqrt(mx*mx + my*my) >= 2: # more than two steps away
        mx = min(mx, 1)
        my = min(my, 1)
        if mx > my:
            tail = (tail[0] + dx, tail[1])
        elif mx < my:
            tail = (tail[0], tail[1] + dy)
        else:
            tail = (tail[0] + dx, tail[1] + dy)
    return tail
```

in rust by Christopher Luu
```
if t.x == h.x || t.y == h.y {
    t.x = (t.x + h.x) / 2;
    t.y = (t.y + h.y) / 2;
} else {
    t.x = t.x + if t.x < h.x { 1 } else { -1 };
    t.y = t.y + if t.y < h.y { 1 } else { -1 };
}
```

in kotlin by Rob Fletcher
```
fun drag(head: Coordinate, next: Coordinate): Coordinate {
  val diff = head - next
  return if ((-1..1).run { diff.x in this && diff.y in this }) {
    next
  } else {
    next.run {
      when {
        diff.x > 0 -> right()
        diff.x < 0 -> left()
        else -> this
      }
    }.run {
      when {
        diff.y > 0 -> down()
        diff.y < 0 -> up()
        else -> this
      }
    }
  }
}
```

in python by Amjith Ramanujam
```
 if abs(self.h.x - self.t.x) > 1 or abs(self.h.y - self.t.y) > 1:
    self.t.x += min(abs(self.h.x - self.t.x), 1) * sgn(self.h.x - self.t.x)
    self.t.y += min(abs(self.h.y - self.t.y), 1) * sgn(self.h.y - self.t.y)
```
