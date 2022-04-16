const co2_reduction = JSON.parse(document.getElementById('co2_reduction').textContent);
console.log(co2_reduction)
const car_offset = JSON.parse(document.getElementById('car_offset').textContent);
console.log(car_offset)
const tree_offset = JSON.parse(document.getElementById('tree_offset').textContent);
console.log(tree_offset)
const sapling_offset = JSON.parse(document.getElementById('sapling_offset').textContent);
console.log(sapling_offset)

document.getElementById("f1text").innerHTML = co2_reduction.concat(" kg of carbon.")
document.getElementById("f2text").innerHTML = car_offset.concat(" cars taken off the road for a year.")
document.getElementById("f3text").innerHTML = tree_offset.concat(" full grown trees or ").concat(sapling_offset).concat(" saplings.")
