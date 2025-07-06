const mainContent = document.getElementById("main-content");
const filePicker = document.getElementById("file-picker");

mainContent.addEventListener("click", event => {
    if (!event.target.matches("#top-section, #top-section *"))
        filePicker.click()
})

document.documentElement.addEventListener("dragover", event => {
    const { dataTransfer } = event
    event.preventDefault()

    const dragValid = dataTransfer.items.length === 1

    dataTransfer.dropEffect = dragValid ? "copy" : "none"
    dataTransfer.effectAllowed = dragValid ? "copy" : "none"
    console.log(event)
})

document.documentElement.addEventListener("drop", event => {
    event.preventDefault()
    // Use DataTransferItemList interface to access the file(s)
    ;[...event.dataTransfer.items].forEach((item, i) => {
        // If dropped items aren't files, reject them
        if (item.kind === "file") {
            const file = item.getAsFile();
            console.log(`… file[${i}].name = ${file.name}`);
        }
    });
})