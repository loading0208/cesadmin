const load = document.querySelector(".box-load")
const btn = document.querySelector(".btnloader")

const form = document.getElementById('quickForm')
const dateleavestart = document.getElementById('dateleavestart')
const dateleaveend = document.getElementById('dateleaveend')
const leavenumd = document.getElementById('leavenumd')
const leavenumh = document.getElementById('leavenumh')
const causedetail = document.getElementById('causedetail')
const headuser = document.getElementById('headuser')
const manageruser = document.getElementById('manageruser')
const radio1 = document.getElementById('customRadio1')
const radio2 = document.getElementById('customRadio2')
const radio3 = document.getElementById('customRadio3')
const radio4 = document.getElementById('customRadio4')



btn.addEventListener("click", function(e) {
  if (dateleavestart.value, dateleaveend.value, leavenumd.value, leavenumh.value, causedetail.value, headuser.value, manageruser.value === '') {

  } else if (radio1.checked === true || radio2.checked=== true || radio3.checked=== true || radio4.checked === true) {
    load.classList.add("loader_page");
  } else if (radio1.checked === false && radio2.checked=== false && radio3.checked=== false && radio4.checked === false) {

  }else {
    load.classList.add("loader_page");
  }
});
