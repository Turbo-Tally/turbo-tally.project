

export class Helpers 
{
    static normalizeDate(date) { 
        return date + " 00:00:00"
    }

    static dateString(datetime) {
        let date = new Date(datetime)
        return date.toISOString().split('T')[0]
    }
}