
function updateUserOrder(itemId, action) {
	console.log('User is authenticated, sending data...')

	var url = '/order/update_item/'

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({ 'itemId': itemId, "action": action })
	})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			if (action == 'edit') {
				changeData(data);
			} else {
				location.reload()
			}
		});
}

function changeData(data) {
	console.log(data);
	document.querySelector('#addToCart').innerText = 'Update';
	document.getElementById("product_id").value = data.order_item.product;
	document.getElementById("product_token").value = data.product_token;
	document.getElementById("item_id").value = data.order_item.id;
	document.getElementById("package").value = data.order_item.package;
	if (data.order_item.package) {
		document.getElementById("day").required = true;
		document.getElementById("time").required = true;
		document.getElementById("product_div").style.display = "none";
		for (i = 0; i < packageDivs.length; i++) {
			var temp = packageDivs[i];
			temp.style.display = "block";
		}
		document.getElementById("day").value = data.order_item.day;
		document.getElementById("time").value = data.order_item.time;
		document.getElementById("leg").value = data.order_item.leg;
		document.getElementById("shoulder").value = data.order_item.shoulder;
		document.getElementById("package_price").value = data.order_item.price;
	}
	document.getElementById("product_price").value = data.order_item.price;
	document.getElementById("discount").value = data.order_item.discount;

}

// function changeType(type) {
// 	console.log(type);
// 	document.getElementById("type").value = type;
// 	if (type == 'C') {
// 		div0.style.display = "none";
// 		div1.style.display = "none";
// 		div2.style.display = "block";
// 	} else if (type == 'G') {
// 		div1.style.display = "block";
// 		div2.style.display = "none";
// 		div0.style.display = "none";
// 	}
// }

// function changePackage(data) {
// 	// document.getElementById("timediv").style.display = "block";
// 	// document.getElementById("datediv").style.display = "block";

// 	console.log(data.package);
// 	if (data.type == 'C') {
// 		console.log("C");
// 		document.getElementById("package2").value = data.package;
// 	} else if (data.type == 'G') {
// 		console.log("G");
// 		document.getElementById("package1").value = data.package;
// 	} else {
// 		console.log("");
// 		document.getElementById("package").value = data.package;
// 	}
// 	document.getElementById("day").value = data.day;
// 	document.getElementById("time").value = data.time;
// }

function clearAll() {
	document.querySelector('#addToCart').innerText = 'Add to Cart';
	document.getElementById("myForm").reset();
	document.getElementById("day").required = false;
	document.getElementById("time").required = false;
	// document.getElementById("timediv").style.display = "none";
	// document.getElementById("datediv").style.display = "none";
}

function fetchCustomer(phone) {
	var url = '/order/get_customer/'

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({ 'phone': phone, })
	})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			if (data) {
				document.getElementById('id_name').value = data.name
				document.getElementById('id_address').value = data.address
			}
		});
}