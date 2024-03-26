/*toggle icon*/ 
let menuIcon = document.querySelector('.bx-menu');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('.bx-x');
    navbar.classList.toggle('active');
}

/*scroll*/
let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');

window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if(top >= offset && top < offset + height) {
            navLinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            });

        };
    });

    let header = document.querySelector('header');

    header.classList.toggle('sticky', window.scrollY > 100);

    
}

// Placeholder user information

var user_full_name = "Andy"; // Ideally, this would come from a server or database
var user_username = "AndyUser";
var user_email = "andy@example.com";
var password = "Andy1234";
var bio = "verginia beach";

document.addEventListener('DOMContentLoaded', function(){
    document.getElementById('name').value = user_full_name;
    document.getElementById('username').value = user_username;
    document.getElementById('email').value = user_email;
    document.getElementById('password').value = password;
    document.getElementById('bio').value = bio;
});
