from js import console
from pyodide import create_proxy 

console.log('starting pyScript')


gridColumns = 3
gridRows = 3
grid = []
g = []

noteHeaderLimit = 30
noteBodyTextLimit = 1000
noteFormHeightOpen = '25%'
noteFormHeightClose = '8%'
noteInputHeight = '45px'


imageDict = ['.jpg', '.jpeg', '.png', '.gif', 'image']

global inputDivFlag
inputDivFlag = 0


### Building Grid Matrix [[0, 0, 0], [0, 0, 0], ...]
for c in range(gridRows):
    for r in range(gridColumns):
        g.append(0)
    grid.append(g)
    g =[]

def checkIfImage(url=''):
    checkImage=[]
    for i in imageDict:
        if i in url.lower():
            checkImage.append(True)
    return set(checkImage)      

def getDomainFromHTTP(str=''):
    if 'http' in str.lower():
        urlSplit = str.split('/')
        return urlSplit[2]
    else:
        return str

def removeNote(e, **args):
    # console.log(str(e.target.parentNode.parentNode.parentNode.id))
    colId = e.target.parentNode.parentNode.parentNode.id
    noteId = e.target.parentNode.parentNode.id
    note = document.getElementById(noteId)
    note.remove()
    r = int(noteId.split('-')[0][2])-1
    c = int(noteId.split('-')[1][1])-1
    console.log("GRID:",str(r), str(c))
    grid[r][c] = 0

def createNoteElement(e,**args):
    global inputDivFlag

    # console.log('inputDivFlag:' , str(inputDivFlag))

    if modal.style.display == 'block' and document.activeElement.id == body.id:
        console.log('OPEN!!')
        closeModal(e)
    
    noteInput = document.getElementById('input')
    noteDesc = noteInput.value

    # check if input div is open (title & description)
    #e.stopPropagation()
    # if noteDesc == '' and (e.target.id not in ['inputTitle','input']) and inputDivFlag == 1:
    if noteDesc == '' and document.activeElement.id not in ['inputTitle','input']:
        createNoteTitle.style.display = 'none'
        closeNoteInput.style.display = 'none'
        createNoteInput.style.height = noteInputHeight
        createNoteInput.value = createNoteTitle.value = ''
        createNoteForm.style.height = noteFormHeightClose
        # pass
    elif noteDesc and (e.target.id not in ['inputTitle','input']):
        createNoteFlag = 1
        for c,col in enumerate(grid):
            for r,row in enumerate(col):
                if row == 0 and createNoteFlag:
                    console.log('createNote')
                    cNote=c+1
                    rNote=r+1
                    x = document.getElementById('col' + str(rNote))
                    note = document.createElement('div')    
                    noteId = '_r' + str(cNote) + '-c' + str(rNote)
                    note.id = noteId

                    noteHeader = document.createElement('div')
                    noteHeader.InnerHTML = 'igal Emona'

                    noteHeaderBtn = document.createElement('span')
                    noteHeaderBtn.className = 'close'
                    buttonXid = 'buttonX' + str(noteId)
                    noteHeaderBtn.id = buttonXid
                    noteHeaderBtn.innerHTML = '&times;'

                    noteBody = document.createElement('div')
                    noteBody.className = 'card-body'
                    bodyNote = 'bodyNote' + str(noteId)
                    noteBody.id = bodyNote

                    noteBodyTitle = document.createElement('h5')
                    noteBodyTitle.className = 'card-title'
                    noteBodyTitleId = 'cardTitle' + str(noteId)
                    noteBodyTitle.id = noteBodyTitleId

                    if checkIfImage(url=noteDesc.lower()):
                        noteType = 'image'
                    elif 'http' in noteDesc[0:10].lower():
                        noteType = 'url'
                    else:
                        noteType = 'note'

                    noteDesc.replace('\n', '<br>')

                    if createNoteTitle.value == '':
                        inputHeader = getDomainFromHTTP(str=noteDesc[0:noteHeaderLimit])
                    else:
                        inputHeader = createNoteTitle.value

                    if noteType == 'image':
                        noteHeader.className = 'card-header d-flex justify-content-between align-items-center snoteHeaderImage'
                        note.setAttribute('data-note-type', 'IMG')
                        noteBodyTitle.innerHTML = inputHeader
                        note.className = 'card text-dark snoteImage shadow-sm my-3'
                        noteBodyImage = document.createElement('img')
                        noteBodyImage.setAttribute('src', str(noteDesc))
                        noteBodyText = document.createElement('a')
                        noteBodyText.setAttribute('href', str(noteDesc))
                        noteBodyText.setAttribute('target', '_blank')
                        noteBodyText.innerTEXT = 'asdasd'
                    elif noteType == 'url':
                        noteHeader.className = 'card-header d-flex justify-content-between align-items-center snoteHeaderUrl'
                        note.setAttribute('data-note-type', 'URL')
                        noteBodyTitle.innerHTML = inputHeader
                        note.className = 'card text-dark snoteUrl shadow-sm my-3'
                        noteBodyImage = document.createElement('img')
                        noteBodyImage.setAttribute('src', str(noteDesc))
                        noteBodyText = document.createElement('a')
                        noteBodyText.setAttribute('href', str(noteDesc))
                        noteBodyText.setAttribute('target', '_blank')
                    else:
                        if "1)" in noteDesc:
                            noteBodyTitle.innerHTML = 'List:'
                        else:
                            noteBodyTitle.innerHTML = inputHeader

                        # noteBodyTitle.innerHTML = 'XXXX'
                        noteHeader.className = 'card-header d-flex justify-content-between align-items-center snoteHeader'
                        note.setAttribute('data-note-type', '')
                        note.className = 'card text-dark snote shadow-sm my-3'
                        noteBodyText = document.createElement('p')
                        
                    noteBodyTextId = 'cardText' + str(noteId)
                    noteBodyText.id = noteBodyTextId
                    noteBodyText.className = 'card-text'
                    noteBodyText.innerText = noteDesc[0:noteBodyTextLimit]
                
                    noteBody.append(noteBodyTitle)
                    noteBody.append(noteBodyText)
                    if noteType == 'image':
                        noteBody.append(noteBodyImage)
                    noteHeader.append(noteHeaderBtn)
                    note.append(noteHeader)
                    note.append(noteBody)
                    x.append(note)
                    document.getElementById(buttonXid).addEventListener("click", create_proxy(removeNote))
                    document.getElementById(bodyNote).addEventListener("click", create_proxy(openModal))
                    createNoteFlag=0
                    grid[c][r] = 1
                    noteInput.value = ''
                    createNoteForm.style.height = noteFormHeightClose
                    createNoteTitle.style.display = 'none'
                    closeNoteInput.style.display = 'none'
                    createNoteInput.style.height = '45px'
                    createNoteInput.value = createNoteTitle.value = ''
                    break
    
def updateNoteBodyLines(e, **args):
    getNoteTarget = modal.getAttribute('data-note-target')
    getModalLines = modalBodylines.value
    document.querySelector(getNoteTarget).innerText = getModalLines
    console.log('--------', getNoteTarget)
    
def openModal(e, **args):
    global modalEnabled
    ## Disable textArea for creating new notes
    createNoteInput.setAttribute('disabled', '') 

    ## Show dialog
    modalDialog.showModal()
    modalEnabled = modal.style.display
    
    if not modalEnabled or modalEnabled == 'none':
        element = str(e.target.id)
        elementId = element.split('_')[1]
        modalEnable = 1
        noteHeaderId = ''
        noteTextId = ''
        console.log('elementId=' + element)

        if 'cardTitle' or 'cardText' in element:
            noteHeaderId = '#cardTitle_' + str(elementId)
            noteTextId = '#cardText_' + str(elementId)

        noteHeader = document.querySelector(noteHeaderId).innerHTML
        noteBody = document.querySelector(noteTextId).innerText
        noteTypeId = '#_' + elementId
        noteType = document.querySelector(noteTypeId).getAttribute('data-note-type')
        console.log(noteType)

        ## Set Modal Header/Body details from note
        modalHeaderSubject.innerText = noteHeader
        modalBodylines.value = noteBody
        modalHeader = document.querySelector('#myModal')
        modalHeader.className = 'modalHeader' + noteType
        modalBodylines.className = 'form-control modalBody' + noteType
        print('modal lines count: ', str(len(modalBodylines.value)))
        ## Set Modal Attributes
        modal.setAttribute('data-note-target', noteTextId)
        ## Set Modal Body size according to note details
        modalCntChars = len(modalBodylines.value)
        if modalCntChars < 100:
            modalBodylines.style.height = "100px";
        elif modalCntChars >= 100 and len(modalBodylines.value) <250:
            modalBodylines.style.height = "150px";
        elif modalCntChars >= 250 and len(modalBodylines.value) < 400:
            modalBodylines.style.height = "300px";
        elif modalCntChars >= 400:
            modalBodylines.style.height = "450px";
        ## Enable Modal
        modal.style.display = 'block'
        modalBodylines.focus()
        ## Add modal listeners
        modalBodylines.addEventListener('change', create_proxy(updateNoteBodyLines))

def closeModal(e, **args):
    modal.style.display = 'none' 
    modalDialog.close()
    createNoteInput.removeAttribute('disabled') 

def textareaInput(e):
    createNoteForm.style.height = noteFormHeightOpen
    createNoteTitle.style.display = 'block'
    closeNoteInput.style.display = 'block'
    createNoteInput.style.height = 'auto'
    scHeigth = e.target.scrollHeight
    createNoteInput.style.height = '{scHeigth}px'.format(scHeigth=scHeigth)

def copyPaste(e, **args):
    if document.activeElement.id != createNoteInput.id \
            and document.activeElement.id != createNoteTitle.id \
                and modal.style.display != 'block':
        createNoteForm.style.height = noteFormHeightOpen
        createNoteTitle.style.display = 'block'
        closeNoteInput.style.display = 'block'
        createNoteInput.style.height = '100px'
        pastedData = e.clipboardData.getData('text')
        createNoteInput.value = pastedData.strip()
        scHeigth = e.target.scrollHeight
        createNoteInput.style.height = '{scHeigth}px'.format(scHeigth=scHeigth)
        
def inputFocusOut(e, **args):
    global inputDivFlag
    
    # // check for focus
    isFocused = (document.activeElement.id == createNoteTitle.id)
    if createNoteInput.value == '' and not isFocused:
        inputDivFlag = 1
        console.log("FOCUS OUT!!", inputDivFlag, document.activeElement.id == createNoteTitle.id)

def debug(e, **args):
    console.log("DEBUG!!")
    console.log(e)
    console.log('tagName:', e.target.tagName)
    console.log('id:', e.target.id)
    console.log('Current active element:', document.activeElement.id)
    console.log('modal status:', modal.style.display)
    console.log(document.activeElement)

### ----------------------------------------------------------- MAIN

## body
body = document.getElementsByTagName('body')[0]
body.addEventListener("paste", create_proxy(copyPaste)) 

## Modal
modal = document.querySelector("#myModal")
modalHeaderSubject = document.querySelector('#noteHeaderSubject')
modalBodylines = document.querySelector('#modalBodyText')
document.querySelector("#closeModal").addEventListener('click', create_proxy(closeModal))
modalDialog = document.getElementById('dialog')

## Inputs
createNoteForm = document.querySelector('.noteForm')
createNoteTitle = document.querySelector('#inputTitle')
createNoteInput = document.getElementById("input")
closeNoteInput = document.getElementById("closeInput")


for event in ["keyup", "focus"]:
    createNoteInput.addEventListener(event, create_proxy(textareaInput)) 

document.addEventListener('click', create_proxy(createNoteElement))
# document.addEventListener('click', create_proxy(debug))