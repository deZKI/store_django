const ajax_filter = document.querySelector('form[id=filter]')
const slider = document.querySelector('.price-slider')
let slider_value = document.querySelector('.filter-price-text')
let param_form = ''

slider.addEventListener('input', function (e){
    slider_value.innerHTML = `Цена <= ${slider.value} руб.`

})
//если ссылку с параметрами будут передавать
$(document).ready(function() {
    ajaxCatalog(ajax_filter.attributes[0].value + window.location.search)
});

function ajaxCatalog(url) {
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => catalog_render(json, url))
        .catch(error => console.error(error))
}

function ajaxPagination(press_value) {
    let url = ajax_filter.attributes[0].value
    url = `${url}?${param_form}page=${press_value}`
    history.pushState(null, null, `?${param_form}page=${press_value}`)
    ajaxCatalog(url)
    document.getElementsByClassName('page-link')[press_value - 1].style.backgroundColor = 'red'
}

ajax_filter.addEventListener('submit', function (e) {
    // Получаем данные из формы
    e.preventDefault()
    let url = this.action
    params = new URLSearchParams(new FormData(this))
    param_form = ''

    let keys = new Set(params.keys())
    for (const key of keys) {
        param_form = key + '=' + params.getAll(key).join(',') + '&' + param_form
    }
    url = `${url}?${param_form}`
    history.pushState(null, null, `?${param_form}`)
    ajaxCatalog(url)
});

function catalog_render(data) {
    // Рендер шаблона
    const divgames = document.querySelector('.col-lg-9>.row')
    const divpagen = document.querySelector('.toolbox>.pagination')

    if (data.games.length === 0) {
        divgames.innerHTML = '<h2>Игр нет, попробуйте поменять параметры поиска</h2>'
        divpagen.innerHTML = ''
    } else {
        let game_list_h = Hogan.compile(htmlGames)
        let game_list = game_list_h.render(data)
        divgames.innerHTML = game_list
        let pagination = ''
        for (let i = 1; i <= data.page_count; i++) {
            pagination = pagination + `<li class="page-item">
                                            <button type="button" class="page-link" onclick="ajaxPagination.call(this, ${i})">  ${i} </button>
                                        </li>`
        }
        divpagen.innerHTML = pagination
    }
}

function apiBasketAdd(game_id) {
    let url = `/api/v1/baskets/`

    fetch(url, {
        method: 'POST',
        body: JSON.stringify({game: game_id, quantity: 1}),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },

    })
        .then(response => {
           location.reload()
        })
}
function apiBasketRemove(basket_id) {
    let url = `/api/v1/baskets/${basket_id}`
    fetch(url, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },

    })
        .then(response => {
            location.reload()
        })
}

function rate(rating, game_id) {
    let url = `/api/v1/rate/${game_id}/${rating}/`
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    }).then(rest => {
            location.reload()
        })
        // rate_lig.innerHTML = ''
}

let htmlGames = '\
{{#games}}\
<div class="col-6 col-md-4 col-xl-3">\
                                <div class="product-default inner-quickview inner-icon">\
                                    <figure>\
                                        <a href="/catalog/game/{{slug}}">\
\
                                            <img src="{{main_image}}" style="height: 200px;width:200px">\
                                        </a>\
                                        <div class="btn-icon-group">\
                                            <button class="btn-icon btn-add-cart" data-toggle="modal"\
                                                    data-target="#addCartModal"><i class="icon-bag" onclick="apiBasketAdd.call(this, {{ id }})"></i></button>\
                                        </div>\
                                        <a href="/catalog/modal-game/{{slug}}" class="btn-quickview"\
                                           title="Quick View">Quick View</a>\
                                    </figure>\
                                    <div class="product-details">\
                                        <h2 class="product-title">\
                                            <a href="/catalog/game/{{slug}}">{{ name }}</a>\
                                        </h2>\
                                        <div class="price-box">\
                                            <span class="product-price">{{ price }}</span>\
                                        </div><!-- End .price-box -->\
                                    </div><!-- End .product-details -->\
                                </div>\
                 <div class="ratings-container">\
         <h5 class="card-title">Средняя оценка: {{ average_rating }}\
        </h5>\
        </div>\
     </div>\
{{/games}}'

