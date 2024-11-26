from transformers import AutoTokenizer, pipeline, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM

def feel(text):
    tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\TANHX.DESKTOP-BJG7USL\Documents\Python Scripts\Whatsapp Recap\multisenti") 
    model=AutoModelForSequenceClassification.from_pretrained (r"C:\Users\TANHX.DESKTOP-BJG7USL\Documents\Python Scripts\Whatsapp Recap\multisenti")
    feeler =pipeline("text-classification",model=model, device=-1, tokenizer=tokenizer)
    return(feeler(text))

def summarise(text):
    tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\TANHX.DESKTOP-BJG7USL\Documents\Python Scripts\Whatsapp Recap\Summariser") 
    model=AutoModelForSeq2SeqLM.from_pretrained (r"C:\Users\TANHX.DESKTOP-BJG7USL\Documents\Python Scripts\Whatsapp Recap\Summariser")
    summarise =pipeline("summarization",model=model, device=-1, tokenizer=tokenizer)

    tokens=tokenizer.tokenize(text)
    # Split the tokens into chunks
    chunks = [tokens[i:i + 1000] for i in range(0, len(tokens), 1000)]

    # Convert token chunks back to strings
    chunks_text = [tokenizer.convert_tokens_to_string(chunk) for chunk in chunks]

    result=summarise(chunks_text)

    while len(result)>1:
        text=''
        for i in result:
            text+=i['summary_text']
        print(text)
        result=summarise(text)
    return(result)

