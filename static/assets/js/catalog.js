"use strict"
const catalog_games = document.querySelector('.col-lg-9>.row')
const catalog_pagination = document.querySelector('.toolbox>.pagination')
const filter = document.querySelector('form[id=filter]')
const slider = document.querySelector('.price-slider')
let slider_value = document.querySelector('.filter-price-text')
let timerId;
let param_form = ''

slider.addEventListener('input', function (e){
    slider_value.innerHTML = `Цена <= ${slider.value} руб.`

})
$(document).ready(function () {
    fetchCatalog(filter.attributes[0].value + window.location.search)
});

class Game {
    constructor(id, name, slug, main_image, price, average_rating) {
        this.id = id
        this.name = name
        this.slug = slug
        this.main_image = main_image
        this.price = price
        if (average_rating === -1) {
            this.average_rating = '<br>Игра не оценена'
        } else {
            this.average_rating = average_rating
        }
    }

    render() {
        return `<div class="col-6 col-md-4 col-xl-3">
            <div class="product-default inner-quickview inner-icon">
                <figure>
                    <a href="/catalog/game/${this.slug}">
                        <img src="${this.main_image}" style="height: 200px;width:200px">
                    </a>
                </figure>
                <div class="product-details">
                    <h2 class="product-title">
                        <a href="/catalog/game/${this.slug}">${this.name}</a>
                    </h2>\
                    <div class="price-box">\
                        <span class="product-price">${this.price}</span>
                    </div><!-- End .price-box -->
                </div>
                <!-- End .product-details -->
            </div>
            <div class="ratings-container">
                <h5 class="card-title">Средняя оценка:${this.average_rating}
                </h5>
            </div>
        </div>`
    }
}

let events = ["click", "change"]
events.forEach(function (event){
    filter.addEventListener(event, function (event) {
        clearTimeout(timerId);
        let url = this.attributes[0].value
        let params = new URLSearchParams(new FormData(this))
        let keys = new Set(params.keys())
        param_form = ''
        for (const key of keys) {
            param_form = key + '=' + params.getAll(key).join(',') + '&' + param_form
        }
        url = `${url}?${param_form}`
        timerId = setTimeout(function () {
            fetchCatalog(url)
            history.pushState(null, null, `?${param_form}`)
        }, 500)
})
})

function fetchCatalog(url) {
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => renderCatalog(json, url))
        .catch(error => console.error(error))
}

function renderCatalog(data) {
    catalog_games.innerHTML = ''
    catalog_pagination.innerHTML = ''
    if (data.games.length === 0) {
        catalog_games.innerHTML = '<h2>Игр нет, попробуйте поменять параметры поиска</h2>'
    } else {
        for (let g of data.games) {
            let game = new Game(g.id, g.name, g.slug, g.main_image, g.price, g.average_rating)
            catalog_games.insertAdjacentHTML('beforeend', game.render())
        }
        let pagination = ''
        for (let i = 1; i <= data.page_count; i++) {
            pagination = pagination + `<li class="page-item">
                                            <button type="button" class="page-link" onclick="ajaxPagination.call(this, ${i})">  ${i} </button>
                                        </li>`
        }
        catalog_pagination.innerHTML = pagination
    }
}

function ajaxPagination(press_value) {
    let url = filter.attributes[0].value
    url = `${url}?${param_form}page=${press_value}`
    history.pushState(null, null, `?${param_form}page=${press_value}`)
    fetchCatalog(url)
    document.getElementsByClassName('page-link')[press_value - 1].style.backgroundColor = 'red'
}