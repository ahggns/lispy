begin
(define factorial n 
    (if (eq n 1) 
        1 
        (* (factorial (- n 1)) n)))
(factorial 5)
