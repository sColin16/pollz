function addOption(){
    createForm = document.getElementById('create-form');
    optionTemplate = createForm.getElementsByClassName('option-field')[0];
    addButton = document.getElementById('add-option');
    
    newOption = optionTemplate.cloneNode(true);
    newOption.childNodes[0].name = 'options[]';
    newOption.childNodes[0].required = true;
    newOption.style = '';
    
    createForm.insertBefore(newOption, addButton);
}

document.getElementById('add-option').addEventListener('click', addOption);
