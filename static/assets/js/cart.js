const cartProductsList = document.querySelector('.dropdown-cart-products')
const addButton = document.querySelector(".add-cart");
const totalSumCart = document.querySelector(".dropdown-cart-total")
const totalQuantityCart = document.querySelectorAll(".cart-count")

class Basket {
    constructor(id, name, price, quantity, game_url, img) {
        this.id = id
        this.name = name
        this.price = Number(price)
        this.quantity = quantity
        if (typeof(game_url) === "string"){
            this.game_url = game_url
        }
        else {
            this.game_url = game_url.href
        }
        this.img = img
    }

    generateCartProduct = () => {
        return `
		<div class="product">
             <div class="product-details">
                <h4 class="product-title">
                     <a href="${this.game_url}">${this.name}</a>
                </h4>

                <span class="cart-product-info">
                <span class="cart-product-qty">${this.price}руб.</span>
                     <br>
                     <button onclick="apibasket_inc_dec.call(this, ${ this.id }, 1)">+</button>
                            <span class="cart-product-qty">кол:${this.quantity}</span>
                     <button onclick="apibasket_inc_dec.call(this, ${ this.id }, -1)">-</button>
                </span>
                </div><!-- End .product-details -->

                <figure class="product-image-container">
                	<a href="${this.game_url}"class="product-image">
                   		 <img src="${this.img}" alt="product">
                    </a>
                     <button class="btn-remove" title="Remove Product"
                        onclick="apiBasketRemove.call(this, ${this.id})"><i
                   	 class="icon-retweet"></i></button>
                </figure>
         </div><!-- End .product -->
	`;
    };
}

class Cart {
    _baskets = []
    constructor() {
        this.total_sum = 0
        this.total_quantity = 0
        if (getCookie('is_logged') === 'true') {
            ['baskets' , 'total_quantity', 'total_sum'].forEach((item) =>{
                localStorage.removeItem(item)
            })
        }
        else{
            this._getLocalStorage()
            this.renderCart()
            this._set_total_values()
        }
    }
    _set_total_values(){
        totalSumCart.innerHTML = `<span>Итог:</span><span class="cart-total-price">${this.total_sum} руб.</span>`
        totalQuantityCart.forEach((quantity) => {
            quantity.innerHTML = this.total_quantity
        })
    }
    _setLocalStorage() {
        localStorage.setItem('baskets', JSON.stringify(this._baskets))
        localStorage.setItem('total_sum', this.total_sum)
        localStorage.setItem('total_quantity', this.total_quantity)
    }
    _insert(basket){
        cartProductsList.insertAdjacentHTML('afterbegin', basket.generateCartProduct());
    }
    _getLocalStorage() {
        const data = JSON.parse(localStorage.getItem("baskets"));
        this.total_sum = localStorage.getItem('total_sum') | 0
        this.total_quantity = localStorage.getItem('total_quantity') | 0
        if (!data) return;
        this._baskets = data;
    }
    isInCart(game_id){
        const data = JSON.parse(localStorage.getItem("baskets"));
        if (!data) return false;
        for (let game of data) {
            if (game.id === game_id){
                return true
            }
        }
        return false
    }
    renderCart(){
        cartProductsList.innerHTML = ''
        this._baskets.forEach((game) => {
          let basket = new Basket(game.id, game.name, game.price, game.quantity, game.game_url, game.img)
          this._insert(basket);
        });

  }
	addBasket(game_id){
        alert('добавлена игра')
        let price = document.querySelector('.product-price').textContent.replace(' руб.', '')
        price = Number(price.replace(',', '.'))

        if (this.isInCart(game_id) === true ){
            const data = JSON.parse(localStorage.getItem("baskets"));
            this.total_quantity = this.total_quantity + 1
            this.total_sum = this.total_sum + price
            this._baskets = []
            data.forEach((game) => {
                if (game.id === game_id){
                    let basket = new Basket(game.id, game.name, game.price+price, game.quantity+1, game.game_url, game.img)
                    this._baskets.push(basket)
                }
                else{
                    let basket = new Basket(game.id, game.name, game.price, game.quantity, game.game_url, game.img)
                    this._baskets.push(basket)
                }
            });
            this.renderCart()
        }
        else {
            let name = document.querySelector('.product-title').textContent
            let img = document.querySelector('#main_img').getAttribute('src')
            let game_url = window.location
            let basket = new Basket(game_id, name, Number(price), 1, game_url, img)
            this.total_sum = this.total_sum + Number(price)
            this.total_quantity = this.total_quantity + 1
            this._baskets.push(basket)
            this._insert(basket)
        }
        this._setLocalStorage()
        this._set_total_values()
	}
    decreaseBasket(game_id) {
        alert('уменьшено количество')
        let price = document.querySelector('.product-price').textContent.replace(' руб.', '')
        price = Number(price.replace(',', '.'))

        if (this.isInCart(game_id) === true) {
            const data = JSON.parse(localStorage.getItem("baskets"));
            this.total_quantity = this.total_quantity - 1
            this.total_sum = this.total_sum - price
            this._baskets = []
            data.forEach((game) => {
                if (game.id === game_id) {
                    let basket = new Basket(game.id, game.name, game.price - price, game.quantity - 1, game.game_url, game.img)
                    this._baskets.push(basket)
                } else {
                    let basket = new Basket(game.id, game.name, game.price, game.quantity, game.game_url, game.img)
                    this._baskets.push(basket)
                }
            });
            this.renderCart()
        }
        this._setLocalStorage()
        this._set_total_values()
    }
    removeBasket(game_id){
        alert('убрана игра')
        const data = JSON.parse(localStorage.getItem("baskets"));
        this._baskets = []
        data.forEach((game) => {
            if (game.id === game_id){
                this.total_sum =  this.total_sum - game.price
                this.total_quantity = this.total_quantity - game.quantity
                return
            }
            let basket = new Basket(game.game_id, game.name, game.price, 1, game.game_url, game.img)
            this._baskets.push(basket)
    });
        this._setLocalStorage()
        this.renderCart()
        this._set_total_values()
    }
}

const cart = new Cart()

function apiBasketAdd(game_id) {
    if (getCookie('is_logged') === 'true') {
        let url = `/api/v1/baskets/`
        localStorage.removeItem('baskets')
        fetch(url, {
            method: 'POST',
            body: JSON.stringify({game: game_id, quantity: 1}),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },

        })
            .then(response => {
                if (response.status === 201) {
                    location.reload()
                }
            })
    } else {
        cart.addBasket(game_id)
        document.cookie = `basket=${getCookie('basket')} ${game_id};path=/`
    }
}
function apibasket_inc_dec(basket_id, count) {
    if (getCookie('is_logged') === 'true') {
        let url = `/api/v1/baskets/${basket_id}/`
        fetch(url, {
        method: 'PATCH',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({quantity: count}),
        })
        .then(response => {
            location.reload()
        })

    } else {
        if (count < 0){
            cart.decreaseBasket(basket_id)
            let basket_cookie = remove_first_occurrence(getCookie('basket'), String(basket_id))
             document.cookie = `basket=${basket_cookie};path=/`
        }
        else {
            cart.addBasket(basket_id)
            document.cookie = `basket=${getCookie('basket')} ${basket_id};path=/`
        }
    }

}
function apiBasketRemove(basket_id) {
    if (getCookie('is_logged') === 'true') {
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

    } else {
        cart.removeBasket(basket_id)
        let basket_cookie = remove_first_occurrence(getCookie('basket'), String(basket_id))
        document.cookie = `basket=${basket_cookie};path=/`
    }

}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : ''
}

function apiWistAdd(game_id) {
    let url = '/api/v1/wish/'
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({game: game_id}),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    })
        .then(response => {
            if (response.status === 201) {
                alert('Игра добавилась в список желаний')
            } else {
                alert('Не удалось добавить в список желаний, возможно, ее уже добавили ')
            }
        })
}

function apiWishRemove(wish_id) {
    let url = `/api/v1/wish/${wish_id}`
    fetch(url, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    }).then(response => {
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

function remove_first_occurrence(str, searchstr) {
    var index = str.indexOf(searchstr);
    if (index === -1) {
        return str;
    }
    return str.slice(0, index) + str.slice(index + searchstr.length);
}