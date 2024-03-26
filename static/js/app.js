
function c(v,txt) {
    console.log(v,txt)
}


class chat {
    constructor() {
        this.text = ""
        this.endpoint = "/api/getAnswerFromAi"
        this.questions = []
        this.answers = []
        this.chatContainer = document.querySelector("#chat-container")
    }

    sendQuestion() {
        c(this.text, 'sendQuestion')
        var self = this
        $.ajax(
            {
            type: 'POST'
            , url: this.endpoint
            , data: { text: this.text}
            , success: function(d)  {
                self.answers.push(d)
                c('success', 'sendQuestion')
                c(d, 'Answer')
                self.pushQandA()
            }
            , error: function() {
                c('error', 'sendQuestion')
            }
        })
    }
    showResponse(data) {
        c(data, 'showResponse')
    }
    setupGUI() {
        $('#Input_Question').keyup(function(e){
            if(e.keyCode == 13) {
                $("#Btn_SendQuestion").click()
            }
        })
        $("#Btn_SendQuestion").click(() => {
            this.text = $("#Input_Question").val()
            this.questions.push(this.text)
            this.sendQuestion()
            $("#Input_Question").val("")
        })
        $("#DisplayChat").html("")
        this.dashboard = $("#DisplayChat")
    }
    pushQandA() {
        const _qaTemplate = document.querySelector("#newQA")
        const qa = _qaTemplate.content.cloneNode(true)
        const user = qa.querySelector(".userdiv")
        const content = qa.querySelector(".contentdiv")
        user.innerHTML = "User:"
        content.innerHTML = this.questions[this.questions.length - 1]
        const botAnswer = qa.querySelector(".botcontent")
        botAnswer.innerHTML = this.answers[this.answers.length - 1]

        this.chatContainer.appendChild(qa)

    }
}



let chat1 = new chat()
chat1.setupGUI()



