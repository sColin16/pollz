function addOption(){
    createForm = document.getElementById('create-form');
    optionTemplate = createForm.getElementsByClassName('option-field')[0];
    addButton = document.getElementById('add-option');
    
    newOption = optionTemplate.cloneNode(true);
    
    createForm.insertBefore(newOption, addButton);
}

document.getElementById('add-option').addEventListener('click', addOption);
