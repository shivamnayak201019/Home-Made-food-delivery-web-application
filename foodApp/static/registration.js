fname=document.getElementById('fname');
lname=document.getElementById('lname');
phn=document.getElementById('phn');
eid=document.getElementById('eid');
pass=document.getElementById('pass');

fname.addEventListener('blur',()=>{
    regex=/^[a-zA-Z]{2,10}$/;
    str=fname.value;
    console.log(regex,str);
    if(regex.test(str)){
        fname.classList.remove('is-invalid')
    }
    else{
        fname.classList.add('is-invalid')
    }

})
lname.addEventListener('blur',()=>{
    regex=/^([a-zA-Z]){2,10}$/;
    str=lname.value;
    console.log(regex,str);
    if(regex.test(str)){
        lname.classList.remove('is-invalid')
    }
    else{
        lname.classList.add('is-invalid')
    }

})

phn.addEventListener('blur',()=>{
    regex=/^[1-9]([0-9]){9}$/;
    str=phn.value;
    console.log(regex,str);
    if(regex.test(str)){
        phn.classList.remove('is-invalid')
    }
    else{
        phn.classList.add('is-invalid')
    }

})

eid.addEventListener('blur',()=>{
    regex=/^([a-zA-Z0-9]+)[@]([a-z]+)[\.]([a-z]){2,3}$/;
    str=eid.value;
    console.log(regex,str);
    if(regex.test(str)){
        eid.classList.remove('is-invalid')
    }
    else{
        eid.classList.add('is-invalid')
    }

})
pass.addEventListener('blur',()=>{
    regex=/^([_@#a-zA-Z0-9]){5,10}$/;
    str=pass.value;
    console.log(regex,str);
    if(regex.test(str)){
        pass.classList.remove('is-invalid')
    }
    else{
        pass.classList.add('is-invalid')
    }

})