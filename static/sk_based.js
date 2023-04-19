let g_stop = false

function get_cards(cards_strings){
    let splited_cards = cards_strings.split("\n")
    let cards = []

    for (let i = 0; i < splited_cards.length; i++){
        let card = splited_cards[i].split("|")
        cards.push({
            "ccn": card[0],
            "exp_m": card[1],
            "exp_y": card[2],
            "cvc": card[3],
        })
    }
    
    return cards
}

async function charge(){
    let cards = document.getElementById("cards").value
    let parsed_cards = get_cards(cards)

    for (let i = 0; i < parsed_cards.length; i++){
        if(g_stop) break
        let card = parsed_cards[i]
        card["option"] = document.getElementById("option").value
        let res = await fetch("/sk/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(card)
        })

        let data = await res.json()
        console.log(data)
        if (data["status"] == "success"){
            let holder = document.getElementById("charge-cards")
            let div = document.createElement("div")
            div.className = `card p-3 rounded bg-zinc-600 mt-2`
            div.innerHTML = `<p>${card.ccn}|${card.exp_m}|${card.exp_y}|${card.cvc}</p>`
            holder.appendChild(div)
        }
        else {
            let holder = document.getElementById("dead-cards")
            let div = document.createElement("div")
            div.className = `card p-3 rounded bg-zinc-600 mt-2`
            div.innerHTML = `<p>${card.ccn}|${card.exp_m}|${card.exp_y}|${card.cvc}</p>`
            holder.appendChild(div)
        }
    }
}

function stop() {
    g_stop = true
    console.log("stop")
}

function delete_cards() {
    document.getElementById("charge-cards").innerHTML = ""
    document.getElementById("dead-cards").innerHTML = ""
    console.log("clear")
}
