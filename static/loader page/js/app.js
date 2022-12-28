const load = document.querySelector(".box-load");
const btn = document.querySelector(".btnloader");

const form = document.getElementById('quickForm');
const dateleavestart = document.getElementById('dateleavestart');
const dateleaveend = document.getElementById('dateleaveend');
const leavenumd = document.getElementById('leavenumd');
const leavenumh = document.getElementById('leavenumh');
const causedetail = document.getElementById('causedetail');
const headuser = document.getElementById('headuser');
const manageruser = document.getElementById('manageruser');
const leaveother = document.getElementById('leaveother');

const radio1 = document.getElementById('customRadio1');
const radio2 = document.getElementById('customRadio2');
const radio3 = document.getElementById('customRadio3');
const radio4 = document.getElementById('customRadio4');

form.addEventListener("submit", function(e) {
  if (dateleavestart.value == '' || dateleaveend.value == '' || leavenumd.value == '' || leavenumh.value == '' || causedetail.value == '' || headuser.value == '' || manageruser.value == '' || radio1.checked===false && radio2.checked===false&&
      radio3.checked===false&& radio4.checked===false || radio4.checked===true&&leaveother.value=='') {
        Swal.fire(
          'กรุณาไส่ข้อมูลให้ครบ',
          '',
          'warning'
        )
        e.preventDefault();
  } else {
    load.classList.add("loader_page");
  }
});
