None


# API
#### Table of Contents

- [keyboard.mouse.**ButtonEvent**](#keyboard.mouse.ButtonEvent)
- [keyboard.mouse.**DOUBLE**](#keyboard.mouse.DOUBLE)
- [keyboard.mouse.**DOWN**](#keyboard.mouse.DOWN)
- [keyboard.mouse.**LEFT**](#keyboard.mouse.LEFT)
- [keyboard.mouse.**MIDDLE**](#keyboard.mouse.MIDDLE)
- [keyboard.mouse.**MoveEvent**](#keyboard.mouse.MoveEvent)
- [keyboard.mouse.**RIGHT**](#keyboard.mouse.RIGHT)
- [keyboard.mouse.**UP**](#keyboard.mouse.UP)
- [keyboard.mouse.**WheelEvent**](#keyboard.mouse.WheelEvent)
- [keyboard.mouse.**X**](#keyboard.mouse.X)
- [keyboard.mouse.**X2**](#keyboard.mouse.X2)
- [keyboard.mouse.**is\_pressed**](#keyboard.mouse.is_pressed)
- [keyboard.mouse.**press**](#keyboard.mouse.press)
- [keyboard.mouse.**release**](#keyboard.mouse.release)
- [keyboard.mouse.**click**](#keyboard.mouse.click)
- [keyboard.mouse.**double\_click**](#keyboard.mouse.double_click)
- [keyboard.mouse.**right\_click**](#keyboard.mouse.right_click)
- [keyboard.mouse.**move**](#keyboard.mouse.move)
- [keyboard.mouse.**on\_button**](#keyboard.mouse.on_button)
- [keyboard.mouse.**on\_click**](#keyboard.mouse.on_click)
- [keyboard.mouse.**on\_double\_click**](#keyboard.mouse.on_double_click)
- [keyboard.mouse.**on\_right\_click**](#keyboard.mouse.on_right_click)
- [keyboard.mouse.**on\_middle\_click**](#keyboard.mouse.on_middle_click)
- [keyboard.mouse.**wait**](#keyboard.mouse.wait)
- [keyboard.mouse.**get\_position**](#keyboard.mouse.get_position)
- [keyboard.mouse.**hook**](#keyboard.mouse.hook)
- [keyboard.mouse.**unhook**](#keyboard.mouse.unhook)
- [keyboard.mouse.**unhook\_all**](#keyboard.mouse.unhook_all)
- [keyboard.mouse.**record**](#keyboard.mouse.record)
- [keyboard.mouse.**play**](#keyboard.mouse.play)
- [keyboard.mouse.**replay**](#keyboard.mouse.replay) *(alias)*


<a name="keyboard.mouse.ButtonEvent"/>
## class keyboard.mouse.**ButtonEvent**

ButtonEvent(event_type, button, time)


<a name="ButtonEvent.button"/>
### ButtonEvent.**button**

Alias for field number 1


<a name="ButtonEvent.count"/>
### ButtonEvent.**count**(...)

T.count(value) -> integer -- return number of occurrences of value


<a name="ButtonEvent.event_type"/>
### ButtonEvent.**event\_type**

Alias for field number 0


<a name="ButtonEvent.index"/>
### ButtonEvent.**index**(...)

T.index(value, [start, [stop]]) -> integer -- return first index of value.
Raises ValueError if the value is not present.


<a name="ButtonEvent.time"/>
### ButtonEvent.**time**

Alias for field number 2




<a name="keyboard.mouse.DOUBLE"/>
## keyboard.mouse.**DOUBLE**
    = 'double'


<a name="keyboard.mouse.DOWN"/>
## keyboard.mouse.**DOWN**
    = 'down'


<a name="keyboard.mouse.LEFT"/>
## keyboard.mouse.**LEFT**
    = 'left'


<a name="keyboard.mouse.MIDDLE"/>
## keyboard.mouse.**MIDDLE**
    = 'middle'


<a name="keyboard.mouse.MoveEvent"/>
## class keyboard.mouse.**MoveEvent**

MoveEvent(x, y, time)


<a name="MoveEvent.count"/>
### MoveEvent.**count**(...)

T.count(value) -> integer -- return number of occurrences of value


<a name="MoveEvent.index"/>
### MoveEvent.**index**(...)

T.index(value, [start, [stop]]) -> integer -- return first index of value.
Raises ValueError if the value is not present.


<a name="MoveEvent.time"/>
### MoveEvent.**time**

Alias for field number 2


<a name="MoveEvent.x"/>
### MoveEvent.**x**

Alias for field number 0


<a name="MoveEvent.y"/>
### MoveEvent.**y**

Alias for field number 1




<a name="keyboard.mouse.RIGHT"/>
## keyboard.mouse.**RIGHT**
    = 'right'


<a name="keyboard.mouse.UP"/>
## keyboard.mouse.**UP**
    = 'up'


<a name="keyboard.mouse.WheelEvent"/>
## class keyboard.mouse.**WheelEvent**

WheelEvent(delta, time)


<a name="WheelEvent.count"/>
### WheelEvent.**count**(...)

T.count(value) -> integer -- return number of occurrences of value


<a name="WheelEvent.delta"/>
### WheelEvent.**delta**

Alias for field number 0


<a name="WheelEvent.index"/>
### WheelEvent.**index**(...)

T.index(value, [start, [stop]]) -> integer -- return first index of value.
Raises ValueError if the value is not present.


<a name="WheelEvent.time"/>
### WheelEvent.**time**

Alias for field number 1




<a name="keyboard.mouse.X"/>
## keyboard.mouse.**X**
    = 'x'


<a name="keyboard.mouse.X2"/>
## keyboard.mouse.**X2**
    = 'x2'


<a name="keyboard.mouse.is_pressed"/>
## keyboard.mouse.**is\_pressed**(button=&#x27;left&#x27;)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L29)

Returns True if the given button is currently pressed. 


<a name="keyboard.mouse.press"/>
## keyboard.mouse.**press**(button=&#x27;left&#x27;)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L34)

Presses the given button (but doesn't release). 


<a name="keyboard.mouse.release"/>
## keyboard.mouse.**release**(button=&#x27;left&#x27;)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L38)

Releases the given button. 


<a name="keyboard.mouse.click"/>
## keyboard.mouse.**click**(button=&#x27;left&#x27;)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L42)

Sends a click with the given button. 


<a name="keyboard.mouse.double_click"/>
## keyboard.mouse.**double\_click**(button=&#x27;left&#x27;)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L47)

Sends a double click with the given button. 


<a name="keyboard.mouse.right_click"/>
## keyboard.mouse.**right\_click**()

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L52)

Sends a right click with the given button. 


<a name="keyboard.mouse.move"/>
## keyboard.mouse.**move**(x, y, absolute=True, duration=0)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L56)


Moves the mouse. If `absolute`, to position (x, y), otherwise move relative
to the current position. If `duration` is non-zero, animates the movement.



<a name="keyboard.mouse.on_button"/>
## keyboard.mouse.**on\_button**(callback, args=(), buttons=(&#x27;left&#x27;, &#x27;middle&#x27;, &#x27;right&#x27;, &#x27;x&#x27;, &#x27;x2&#x27;), types=(&#x27;up&#x27;, &#x27;down&#x27;, &#x27;double&#x27;))

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L90)

Invokes `callback` with `args` when the specified event happens. 


<a name="keyboard.mouse.on_click"/>
## keyboard.mouse.**on\_click**(callback, args=())

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L104)

Invokes `callback` with `args` when the left button is clicked. 


<a name="keyboard.mouse.on_double_click"/>
## keyboard.mouse.**on\_double\_click**(callback, args=())

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L108)


Invokes `callback` with `args` when the left button is double clicked.



<a name="keyboard.mouse.on_right_click"/>
## keyboard.mouse.**on\_right\_click**(callback, args=())

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L114)

Invokes `callback` with `args` when the right button is clicked. 


<a name="keyboard.mouse.on_middle_click"/>
## keyboard.mouse.**on\_middle\_click**(callback, args=())

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L118)

Invokes `callback` with `args` when the middle button is clicked. 


<a name="keyboard.mouse.wait"/>
## keyboard.mouse.**wait**(button=&#x27;left&#x27;, target\_types=(&#x27;up&#x27;, &#x27;down&#x27;, &#x27;double&#x27;))

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L122)


Blocks program execution until the given button performs an event.



<a name="keyboard.mouse.get_position"/>
## keyboard.mouse.**get\_position**()

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L133)

Returns the (x, y) mouse position. 


<a name="keyboard.mouse.hook"/>
## keyboard.mouse.**hook**(callback)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L137)


Installs a global listener on all available mouses, invoking `callback`
each time it is moved, a key status changes or the wheel is spun. A mouse
event is passed as argument, with type either `mouse.ButtonEvent`,
`mouse.WheelEvent` or `mouse.MoveEvent`.

Returns the given callback for easier development.



<a name="keyboard.mouse.unhook"/>
## keyboard.mouse.**unhook**(callback)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L149)


Removes a previously installed hook.



<a name="keyboard.mouse.unhook_all"/>
## keyboard.mouse.**unhook\_all**()

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L155)


Removes all hooks registered by this application. Note this may include
hooks installed by high level functions, such as [`record`](#keyboard.mouse.record).



<a name="keyboard.mouse.record"/>
## keyboard.mouse.**record**(button=&#x27;right&#x27;, target\_types=(&#x27;down&#x27;,))

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L162)


Records all mouse events until the user presses the given button.
Then returns the list of events recorded. Pairs well with [`play(events)`](#keyboard.mouse.play).

Note: this is a blocking function.
Note: for more details on the mouse hook and events see [`hook`](#keyboard.mouse.hook).



<a name="keyboard.mouse.play"/>
## keyboard.mouse.**play**(events, speed\_factor=1.0, include\_clicks=True, include\_moves=True, include\_wheel=True)

[\[source\]](https://github.com/boppreh/keyboard/blob/master/.\keyboard\mouse.py#L176)


Plays a sequence of recorded events, maintaining the relative time
intervals. If speed_factor is <= 0 then the actions are replayed as fast
as the OS allows. Pairs well with [`record()`](#keyboard.mouse.record).

The parameters `include_*` define if events of that type should be inluded
in the replay or ignored.



<a name="keyboard.mouse.replay"/>
## keyboard.mouse.**replay**

Alias for `play`.


