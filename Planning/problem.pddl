(define (problem festival) ; the problem name
(:domain tavern) ; the domain in which the problem takes place
(:objects ; the objects in the problem
    ; reserved parties
    livingstone
    the_fellowship
    mardi_gras
    friends
    vox_machina
    ; drop in parties
    p1
    p2
    p3
    p4
    ; rooms
    suite
    deluxe
    regular
    cellar
    ; sizes
    small
    large
    medium
    ;
    thursday
    friday
    saturday
    sunday
)
(:init ; the initial world state
    ; the parties
    (party livingstone) (party the_fellowship)
    (party p1) (party p2)
    (party mardi_gras) (party friends) (party vox_machina)
    (party p3) (party p4)
    ; the rooms
    (room suite) (room deluxe)
    (room regular) (room cellar)
    ; the sizes
    (size small) (size large)
    (size medium)
    ; the days
    (day thursday) (day friday) (day saturday)
    (day sunday)
    ; the reservations
    (has_reservation livingstone suite thursday)

    (has_reservation livingstone suite friday) 
    (has_reservation mardi_gras cellar friday)
    (has_reservation vox_machina deluxe friday)

    (has_reservation livingstone suite saturday)
    (has_reservation mardi_gras cellar saturday)
    (has_reservation friends regular saturday)
    (has_reservation the_fellowship deluxe saturday)



 
    (has_reservation p3 regular friday)
    (has_reservation p3 cellar thursday)
    (has_reservation p4 regular thursday)
    (has_reservation p2 deluxe thursday)
    (has_reservation p1 suite sunday)
    (has_reservation p3 cellar sunday)
    (has_reservation p4 regular sunday)
    (has_reservation p2 deluxe sunday)


    ; the drop in party sizes
    (is_size p1 small) (is_size p2 large) 
    (is_size p3 medium) (is_size p4 medium)
    ; the room sizes
    (is_size suite small) 
    (is_size deluxe large)
    (is_size regular medium)
    (is_size cellar medium)
    ; the size structure
    (fits small small) (fits small large)(fits small medium)
    (fits medium medium) (fits medium large)
    (fits large large)

    ; thursday is the current day
    (is_current_day thursday)
    ; the day order
    (is_next_day thursday friday) (is_next_day friday saturday)
    (is_next_day saturday sunday)
    ; the rooms are empty and clean
    (is_vacant suite) (is_clean suite) 
    (is_vacant deluxe) (is_clean deluxe)
    (is_vacant regular) (is_clean regular)
    (is_vacant cellar) (is_clean cellar)
)
(:goal ; the end goals
    ; all rooms are booked each day
    ; the parties with reservations were booked accordingly
    (and
        (has_booked_room suite thursday) (has_booked_room deluxe thursday)
        (has_booked_room regular thursday) (has_booked_room cellar thursday)
        (has_booked_room suite friday) (has_booked_room deluxe friday)
        (has_booked_room regular friday) (has_booked_room cellar friday) 
        (has_booked_room suite saturday) (has_booked_room deluxe saturday)
        (has_booked_room regular saturday) (has_booked_room cellar saturday)
        (has_booked_room suite sunday) (has_booked_room deluxe sunday)
        (has_booked_room regular sunday) (has_booked_room cellar sunday)



        (has_booked_party livingstone thursday)
        (has_booked_party livingstone friday)
        (has_booked_party livingstone saturday)

        (has_booked_party mardi_gras friday)
        (has_booked_party mardi_gras saturday)

        (has_booked_party friends saturday)

        (has_booked_party the_fellowship saturday)

        (has_booked_party vox_machina friday)

        

        (has_booked_party p1 sunday)
        (has_booked_party p2 sunday)
        (has_booked_party p3 sunday)
        (has_booked_party p4 sunday)
        (has_booked_party p2 thursday) 
        (has_booked_party p3 thursday) 
        (has_booked_party p4 thursday)
        (has_booked_party p3 friday) 

    )
)

)
