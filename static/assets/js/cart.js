const cartProductsList = document.querySelector('.dropdown-cart-products')
const addButton = document.querySelector(".add-cart");
const totalSumCart = document.querySelector(".dropdown-cart-total")
const totalQuantityCart = document.querySelectorAll(".cart-count")

class Basket {
    constructor(id, name, price, quantity, game_url, img) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.quantity = quantity
        this.game_url = game_url.href
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
                <span class="cart-product-qty">кол:${this.quantity}</span>
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
    renderCart(){
        cartProductsList.innerHTML = ''
        this._baskets.forEach((game) => {
          let basket = new Basket(game.id, game.name, game.price, game.quantity, game.game_url, game.img)
          this._insert(basket);
        });

  }
	addBasket(game_id){
        alert('добавлен')
        let name = document.querySelector('.product-title').textContent
        let price = document.querySelector('.product-price').textContent.replace(' руб.', '')
        let img = document.querySelector('#main_img').getAttribute('src')
        let game_url = window.location

        price = Number(price.replace(',', '.'))
        let basket = new Basket(game_id, name, price, 1, game_url, img)
        this.total_sum = this.total_sum + Number(price)
        this.total_quantity = this.total_quantity + 1

		this._baskets.push(basket)
        this._setLocalStorage()
        this._insert(basket)
        this._set_total_values()
	}
    removeBasket(game_id){
        const data = JSON.parse(localStorage.getItem("baskets"));
        this._baskets = []
        data.forEach((game) => {
            alert(game.id, game_id)
            if (game.id === game_id){
                this.total_sum =  this.total_sum - game.price
                this.total_quantity = this.total_quantity - 1
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
    cart.addBasket(game_id)
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

            })
    } else {

        // #удаление из кук
        document.cookie = `basket=${getCookie('basket')} ${game_id};path=/`
    }
}

function apiBasketRemove(basket_id) {
    cart.removeBasket(basket_id)
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

        })

    } else {

    }

}