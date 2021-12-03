function addToCart(id, name, price, image) {
    event.preventDefault()
    // promise
    fetch('/api/add-to-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'image': image
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        // console.log(data)
        let cartCounter = document.getElementById('cart__counter')
        cartCounter.innerText = data.total_quantity
    })
}

function pay() {
    event.preventDefault()
    
    if (confirm('Ban chac chan thanh toan khong?') == true) {
        fetch('/api/pay', {
            method: 'post'
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            if (data.code === 200)
            location.reload()
        })
    }
}