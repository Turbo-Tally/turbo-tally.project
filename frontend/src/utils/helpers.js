

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
            return Helpers.dateString(dt)
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
}