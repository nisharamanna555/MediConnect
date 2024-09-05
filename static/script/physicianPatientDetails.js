var content = document.getElementById("content");
var currentMedicationsTable = document.getElementById('current');
var pastMedicationsTable = document.getElementById('past');
var popup = document.getElementById('popup');
var popupClose = document.getElementById('popupClose');
popupClose.style.cursor = "pointer";
popupClose.addEventListener("click", (e) => {
    popup.style.display = "none";
});
document.getElementById("addMedication").addEventListener("click", (e) => {
    content.style.display = "none";
    medicationInputs.style.display = "grid";
});
document.getElementById("addCancel").addEventListener("click", (e) => {
    medicationInputs.style.display = "none";
    content.style.display = "grid";
});
var medicationInputs = document.getElementById("medicationInputs");

$(document).ready(function(){
    medicationInputs.style.display = "none";
    createDefaultPage();
});

function getNotes(patient_id, medication_id, callback) { 
    $.ajax({
        url:'/get_patient_notes',
        method:'GET',
        data:{
            patient_id:patient_id,
            medication_id:medication_id
        },
        success:function(notes) {
            callback(notes);
        },
        error:function() {
            console.log("Error fetching notes");
        }
    });
}

function getPhysicianInfo(physician_id, callback) {
    $.ajax({
        url: `/get_physician_info/${physician_id}`,
        method: 'GET',
        success: function(physician) {
            callback(physician);
        },
        error: function() {
            console.log("Error fetching physician info");
        }
    });
}

function getMedicationList(callback) {
    $.ajax({
        url:'/get_medication_list',
        method:'GET',
        success:function(medicationList) {
            callback(medicationList);
        },
        error:function() {
            console.log("Error fetching medication list");
        }
    });
}

function resetPopup() {
    let cautions = document.querySelectorAll('.caution');
    cautions.forEach(function(caution) {
        caution.remove();
    });
    let notes = document.querySelectorAll('.notes');
    notes.forEach(function(note) {
        note.remove();
    });
    let buttons = document.querySelectorAll('.popupButton');
    buttons.forEach(function(button) {
        button.remove();
    });
}

function updateNote(patient_id, medication_id, notes) {
    $.ajax({
        url: "/update_note",
        method: "POST",
        data: {
            patient_id:patient_id,
            medication_id:medication_id,
            notes:notes
        },
        success:function(response) {
            if(response.status === true) {
                console.log("Note updated successfully!");
            } else {
                console.log("Note update failed");
            }
        },
        error:function() {
            console.log("Note update error");
        }
    }).then(function(){
        location.reload();
    });
}

function createDefaultPage() {
    $.ajax({
        url:'/get_patient_medications/'+patient_id.toString(),
        method:'GET',
        success:function(data)
        {
            // add rows for currentMedicationsTable
            if(data[0].length === 0) {
                currentMedicationsTable.innerHTML = "<th>No Medications Found</th>";
            } else {
                let tableAttributes = "<tr>";
                tableAttributes += "<th>Medication name</th>";
                tableAttributes += "<th>Dose</th>";
                tableAttributes += "<th>Frequency</th>";
                tableAttributes += "<th>Days supply</th>";
                tableAttributes += "<th>Prescription valid until</th>";
                tableAttributes += "<th>Prescribed by</th>";
                tableAttributes += "<th>Notes</th>";
                tableAttributes += "</tr>";
                currentMedicationsTable.innerHTML = tableAttributes;
                pastMedicationsTable.innerHTML = tableAttributes;

                for(let i = 0; i < data[0].length; i++) {
                    let rowNum = i + 1;
                    let row = currentMedicationsTable.insertRow(rowNum);
                    let medicationName = row.insertCell(0);
                    medicationName.innerHTML = data[0][i].medication_name;
                    let dose = row.insertCell(1);
                    dose.innerHTML = data[0][i].dosage;
                    let frequency = row.insertCell(2);
                    frequency.innerHTML = data[0][i].frequency;
                    let duration = row.insertCell(3);
                    duration.innerHTML = data[0][i].days_supply;
                    let validTill = row.insertCell(4);
                    validTill.innerHTML = data[0][i].prescription_valid_till;
                    let medicationDate = row.insertCell(5);
                    medicationDate.innerHTML = data[0][i].date_prescribed;
                    let note = row.insertCell(6);
                    note.style.cursor = "pointer";
                    getNotes(patient_id, data[0][i].id, function(notes) {
                        note.textContent = Object.keys(notes).length.toString();
                        note.style.textDecoration = "underline";
                    });
                    note.addEventListener("click", (e) => {
                        resetPopup();
                        getNotes(patient_id, data[0][i].id, function(notes) {
                            if(Object.keys(notes).length == 0){
                                let noteDiv = document.createElement("div");
                                noteDiv.className = "caution";
                                noteDiv.textContent = "No notes written for this medication yet";
                                popup.appendChild(noteDiv);
                            } else {
                                let noteDiv = document.createElement("div");
                                noteDiv.className = "notes";
                                for(const [physician_id, array] of Object.entries(notes)) {
                                    let entry = document.createElement("div");
                                    entry.className = "note";
                                    entry.style.overflow = "auto";
                                    entry.style.wordBreak = "break-word";
                                    getPhysicianInfo(physician_id, function(physician) {
                                        entry.textContent = `Dr. ${physician.first_name} ${physician.last_name}: "${array.note}"`;
                                    });
                                    // entry.id = physician_id;
                                    // entry.textContent = 'physician ' + physician_id + ' wrote: "' + array["note"] + '"';
                                    entry.style.height = "100px";
                                    noteDiv.appendChild(entry);
                                }
                                popup.appendChild(noteDiv);
                            }
                            let popupButton = document.createElement("button");
                            popupButton.className = "popupButton";
                            popupButton.id = "popupButton";
                            popupButton.textContent = "Add Note";
                            popupButton.addEventListener("click", (e) => {
                                resetPopup();
                                let noteInput = document.createElement("textarea");
                                noteInput.className = "input";
                                noteInput.style.height = "80%";
                                noteInput.style.border = "1px solid";
                                noteInput.placeholder = "Type note here";
                                noteInput.maxLength = 510;
                                popup.appendChild(noteInput);
                                let confirmButton = document.createElement("button");
                                confirmButton.className = "popupButton";
                                confirmButton.id = "confirmButton";
                                confirmButton.textContent = "Add Note";
                                confirmButton.addEventListener("click", (e) => updateNote(patient_id, data[0][i].id, noteInput.value));
                                popup.appendChild(confirmButton);
                            });
                            popup.appendChild(popupButton);
                            popup.style.display = "flex"; 
                        });                   
                    });
                }
            }

            // add rows for pastMedicationsTable
            if (data[1].length === 0){
                pastMedicationsTable.innerHTML = "<th>No Medications Found</th>";
            } else {
                for(let i = 0; i < data[1].length; i++) {
                    let rowNum = i + 1;
                    let row = pastMedicationsTable.insertRow(rowNum);
                    let medicationName = row.insertCell(0);
                    medicationName.innerHTML = data[1][i].medication_name;
                    let dose = row.insertCell(1);
                    dose.innerHTML = data[1][i].dosage;
                    let frequency = row.insertCell(2);
                    frequency.innerHTML = data[1][i].frequency;
                    let duration = row.insertCell(3);
                    duration.innerHTML = data[1][i].days_supply;
                    let validTill = row.insertCell(4);
                    validTill.innerHTML = data[1][i].prescription_valid_till;
                    let medicationDate = row.insertCell(5);
                    medicationDate.innerHTML = data[1][i].date_prescribed;
                    let note = row.insertCell(6);
                    note.style.cursor = "pointer";
                    getNotes(patient_id, data[1][i].id, function(notes) {
                        note.textContent = Object.keys(notes).length.toString();
                        note.style.textDecoration = "underline";
                    });
                    note.addEventListener("click", (e) => {
                        resetPopup();
                        getNotes(patient_id, data[1][i].id, function(notes) {
                            if(Object.keys(notes).length == 0){
                                let noteDiv = document.createElement("div");
                                noteDiv.className = "caution";
                                noteDiv.textContent = "No notes written for this medication yet";
                                popup.appendChild(noteDiv);
                            } else {
                                let noteDiv = document.createElement("div");
                                noteDiv.className = "notes";
                                for(const [physician_id, array] of Object.entries(notes)) {
                                    let entry = document.createElement("div");
                                    entry.className = "note";
                                    entry.style.overflow = "auto";
                                    entry.style.wordBreak = "break-word";
                                    getPhysicianInfo(physician_id, function(physician) {
                                        entry.textContent = `Dr. ${physician.first_name} ${physician.last_name}: "${array.note}"`;
                                    });
                                    // entry.id = physician_id;
                                    // entry.textContent = 'physician ' + physician_id + ' wrote: "' + array["note"] + '"';
                                    entry.style.height = "100px";
                                    noteDiv.appendChild(entry);
                                }
                                popup.appendChild(noteDiv);
                            }
                            let popupButton = document.createElement("button");
                            popupButton.className = "popupButton";
                            popupButton.id = "popupButton";
                            popupButton.textContent = "Add Note";
                            popupButton.addEventListener("click", (e) => {
                                resetPopup();
                                let noteInput = document.createElement("textarea");
                                noteInput.className = "input";
                                noteInput.style.height = "80%";
                                noteInput.style.border = "1px solid";
                                noteInput.placeholder = "Type note here";
                                noteInput.maxLength = 510;
                                popup.appendChild(noteInput);
                                let confirmButton = document.createElement("button");
                                confirmButton.className = "popupButton";
                                confirmButton.id = "confirmButton";
                                confirmButton.textContent = "Add Note";
                                confirmButton.addEventListener("click", (e) => updateNote(patient_id, data[1][i].id, noteInput.value));
                                popup.appendChild(confirmButton);
                            });
                            popup.appendChild(popupButton);
                            popup.style.display = "flex"; 
                        });                   
                    });
                }
            }

            let datalist = document.getElementById("medicationName");
            getMedicationList(function(medicationList) {
                Object.keys(medicationList).forEach(function(key) {
                    datalist.innerHTML += "<option value='"+key+"'>"+key+"</option>";
                });
            });
        },
        error:function()
        {
            currentMedicationsTable.innerHTML = "<th>No Medications Found</th>";
            pastMedicationsTable.innerHTML = "<th>No Medications Found</th>";
        }
    });
}