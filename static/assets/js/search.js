document.querySelector('#q').addEventListener("input", function (event) {
    timerId = setTimeout(function () {
        console.log(event.target.value)
        fetch(`/api/v1/games/?search=${event.target.value}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
            .then(response => {
                console.log(response)
                console.log(response.json.games)
            })

        history.pushState(null, null, `?${param_form}`)
    }, 500)
    parent = event.target
    console.log(parent)
    dropdown = ''
    parent.insertAdjacentHTML('afterend', '1212')
    console.log('поиск')
})