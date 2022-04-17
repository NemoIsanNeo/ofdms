    $('#popbar').hide();

function clearCart() {
    cart = JSON.parse(localStorage.getItem('cart'));
    localStorage.clear();
    cart = {};
    updatePopover(cart);
}

updatePopover(cart);

function updatePopover(cart) {
    console.log('We are inside updatePopover');
    var popStr = "";
    popStr = popStr + "<div class='mx-2 my-2'>";
    var i = 1;
    var grandtotal = 0;
    for (var item in cart) {


        var qty = cart[item][0]
        var price = cart[item][2]
        var total = parseInt(qty) * price
        grandtotal = parseInt(grandtotal) + total

        popStr = popStr + "<b>" + i + ".</b>";
        popStr = popStr + cart[item][1] + "   Price : " + cart[item][2] + "... Qty: " + "<b>" + cart[item][0] + "</b>  " + "  Total : " + total + 'Taka' + '<br><br>';
        i = i + 1;
    }

        popStr = popStr + "<b>Grand Total<b/> : " + grandtotal + " Taka<br><br>";
        popStr = popStr + "</div><div class='d-flex justify-content-center'> <a style='padding-right: 10px' href='/checkout'><button class='btn btn-primary' id ='checkout'>Checkout</button></a> <button class='btn btn-primary' onclick='clearCart()' id ='clearCart'>Clear Cart</button>  ";
        popStr = popStr + "</div>"
        console.log(cart)
        console.log(popStr)

        document.getElementById('popcart').innerHTML = popStr
    }


    console.log('working');
    if (localStorage.getItem('cart') == null) {
        var cart = {};
    }
    else {
        cart = JSON.parse(localStorage.getItem('cart'));
        document.getElementById('cart').innerHTML = Object.keys(cart).length;
        updatePopover(cart);

    }
    $('.cart').click(function () {
        var idstr = this.id.toString();
        console.log(idstr);
        if (cart[idstr] != undefined) {
            let qty = cart[idstr][0] + 1;
            let name = document.getElementById('name'+idstr).innerHTML
            let price = parseInt(document.getElementById('price' + idstr).innerHTML)
            cart[idstr] = [qty,name,price];
        }
        else {
           let qty = 1
            let name = document.getElementById('name'+idstr).innerHTML
            let price = parseInt(document.getElementById('price' + idstr).innerHTML)
            cart[idstr] = [qty,name,price];
        }
        console.log(cart);
        localStorage.setItem('cart', JSON.stringify(cart));
        document.getElementById('cart').innerHTML = Object.keys(cart).length;
        updatePopover(cart);

    });


    $('#bin').click(function () {
                $('#popbar').toggle();

    })




var sum = 0;
var total = 0;
if ($.isEmptyObject(cart)) {
    //if object is empty
    mystr = `<p>Your cart is empty, please add some items to your cart before checking out!</p>`
    $('#items').append(mystr);
} else {
    for (item in cart) {
        let name = cart[item][1];
        let qty = cart[item][0];
        let price = cart[item][2]
        sum = price * qty;
        total = total + sum

        mystr = `<li style="justify-content: space-between;" class="list-group-item d-flex justify-content-between align-items-center">
                   <sapan> ${name} - ${price} Taka</sapan>
                    <span class="badge badge-primary badge-pill">${qty}</span>
                </li>`
        $('#items').append(mystr);
    }
    $('#grandtotal').append(total)

}


 $('#itemsJson').val(JSON.stringify(cart));
