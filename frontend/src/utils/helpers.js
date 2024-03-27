

export class Helpers 
{
    static normalizeDate(date) { 
        return date + " 00:00:00"
    }

    static dateString(datetime) {
        let date = new Date(datetime)
        return date.toISOString().split('T')[0]
    }

    static daysAgo(dt) {
        const now = new Date()
        const date = new Date(dt) 
        const diff = now.getTime() - date.getTime()
        const diffDays = diff / (1000 * 3600 * 24); 
        return diffDays;
    }

    static daysAgoText(dt) {
        const ago = Helpers.daysAgo(dt) 
        if (ago == 0) {
            return "Today"
        }
        else if (ago == 1) {
            return "Yesterday"
        }
        else if (ago >= 2 && ago <= 7) {
            return ago + " days ago"
        }
        else if (ago >= 7 && ago <= 14) {
            return "Last Week"
        }
        else if (ago > 14 && ago <= 28) {
            return Math.round(ago / 7) + " weeks ago"
        }
        else {
            const date = new Date(dt) 
            const dateString = date.toString() 
            const tokens = dateString.split(" ") 
            const part = tokens.slice(1, 4)
            part[0] = part[0] + "."
            part[1] = part[1] + ","
            return part.join(" ")
        }
    }

    static timeText(dt) {
        const date = new Date(dt)
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var ampm = hours >= 12 ? 'pm' : 'am';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        minutes = minutes < 10 ? '0'+minutes : minutes;
        var strTime = hours + ':' + minutes + ' ' + ampm;
        return strTime;
    }

    static onScrollBottom(cb) {
        window.addEventListener(
            'scroll', 
            async () => {
                const atBottom = 
                    window.offsetHeight - (innerHeight + pageYOffset) <= 0;
                if(atBottom) {
                    await cb()
                }
            }, 
            {
                passive: true
            }
        )
    }

    static async onContainerScrollBottom(container, cb) {
        container.addEventListener("scroll", async () => {
            const scrollTop = container.scrollTop + container.offsetHeight
            const scrollHeight = container.scrollHeight 

            if (scrollTop + 100 >= (scrollHeight)) {
                await cb()
            }
        });
    }

    static rekey(data, keymap, mapper = {}) {
        const dataRekey = [] 
        for(let i = 0; i < data.length; i++) {
            const dataItem = data[i]
            const dataRekeyItem = {}
            for(let origKey in dataItem) {
                const newKey = keymap[origKey] 
                let value = dataItem[origKey]
                if(newKey in mapper) {
                    value = mapper[newKey](value)
                }
                dataRekeyItem[newKey] = value
            }
            dataRekey.push(dataRekeyItem)
        }
        return dataRekey
    }

    static revalue(data, valuemap, targetKey) {
        const dataRekey = [] 
        for(let i = 0; i < data.length; i++) {
            const dataItem = data[i]
            for(let key in dataItem) {
                let value = dataItem[key]
                if(key == targetKey)  {
                    dataItem[key] = valuemap[value]
                }
            }
            dataRekey.push(dataItem)
        }
        return dataRekey
    }

    static extractChoices(results) {
        const choiceMap = {}
        for(let result of results) {
            choiceMap[result._id] = result.answer_count
        }
        return choiceMap
    }
}