from fastapi import FastAPI
 
app=FastAPI (
    title='AI Text_to_SQL API',
    description='Backend api for the AI-poweredvText-to-SQL system',
    version='0.1.0'
    )

@app.get('/health')
def health_check():
    return{
        'status':'healthy',
        'service':'text to sql api'
    }