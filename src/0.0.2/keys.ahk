; Get command-line arguments (input type and key)
InputType := A_Args[1]  ; e.g., "keydown" or "keyup"
Key := A_Args[2]  ; e.g., "A"

if (InputType = "keydown") {
    ; Simulate key press
    Send(Key "{Down}")
} else if (InputType = "keyup") {
    ; Simulate key release
    Send(Key "{Up}")
}
ExitApp