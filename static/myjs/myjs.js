const form = document.getElementById('form');
const show = document.getElementById('show');

form.addEventListener('submit', function(e) {
  e.preventDefault();
  if (show.value === '') {
    showerror(show, 'กรุณาไส่ข้อมูล');
  } else {
    showsuccess(show);
  }
});

function showerror(input, message) {
  const formcontrol = input.parentElement;
  formcontrol.className = 'form-control error';
}

function showsuccess() {

}
