form1=document.querySelector('.pt-5')
form1.addEventListener('submit',(event)=>{
    event.preventDefault()
    const formdata=new FormData(form1)
    specinp=formdata.get('ufspec')
    console.log(specinp)
    if (specinp=="others"){
        alert("Item Sent for Approval");
        form1.submit(); 
    }
    else{
        form1.submit(); 
    }
})