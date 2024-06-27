

function setRockets(){
    var rockets = document.querySelectorAll('.rocket-element');
    var a = 0

    rockets.forEach((rocket) =>{
        a = a+1
        var paddingRocket = 560 - (a*90)
        console.log(rocket.style.paddingLeft = `${paddingRocket}px`)
    })
}


setRockets();