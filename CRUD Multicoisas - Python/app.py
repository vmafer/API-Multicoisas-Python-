import email
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:*senha*@localhost/multicoisas2'

db = SQLAlchemy(app)

# CONSTRUÇÃO DAS TABELAS COM OS ATRIBUTOS

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    codigo = db.Column(db.Integer())
    nome = db.Column(db.String(128))
    descricao = db.Column(db.String(128))
    categoriaid = db.Column(db.Integer())
    datacriacao = db.Column(db.String(128))
    datamodificacao = db.Column(db.String(128))

class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    produtoid = db.Column(db.Integer())
    quantidade = db.Column(db.Integer())
    datacriacao = db.Column(db.String(128))
    datamodificacao = db.Column(db.String(128))

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    codigo = db.Column(db.Integer())
    nome = db.Column(db.String(128))
    datacriacao = db.Column(db.String(128))
    datamodificacao = db.Column(db.String(128))

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    codigo = db.Column(db.Integer())
    nome = db.Column(db.String(128))
    datanascimento = db.Column(db.String(128))
    email = db.Column(db.String(128))
    datacriacao = db.Column(db.String(128))
    datamodificacao = db.Column(db.String(128))

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    codigo = db.Column(db.Integer())
    valor = db.Column(db.String(128))
    datavenda = db.Column(db.String(128))
    clienteid = db.Column(db.Integer())
    datacriacao = db.Column(db.String(128))
    datamodificacao = db.Column(db.String(128))

    # FUNÇÕES PARA TRANSFORMAÇÃO DOS ATRIBUTOS EM JSON 

    def to_json(Produto):
        return{"id":Produto.id, "codigo": Produto.codigo, "nome": Produto.nome, "descricao": Produto.descricao, "categoriaid": Produto.categoriaid, "datacriacao": Produto.datacriacao, "datamodificacao": Produto.datamodificacao}
    
    def to_json(Estoque):
        return{"id":Estoque.id, "produtoid": Estoque.produtoid, "quantidade": Estoque.quantidade, "datacriacao": Estoque.datacriacao,"datamodificacao": Estoque.datamodificacao}

    def to_json(Categoria):
        return{"id":Categoria.id, "cogido": Categoria.codigo, "nome": Categoria.nome, "datacriacao": Categoria.datacriacao,"datamodificacao": Categoria.datamodificacao}

    def to_json(Cliente):
        return{"id":Cliente.id, "codigo": Cliente.codigo, "nome": Cliente.nome, "datanascimento": Cliente.datanascimento, "email": Cliente.email, "datacriacao": Cliente.datacriacao, "datamodificacao": Cliente.datamodificacao}  

    def to_json(Venda):
        return{"id":Venda.id, "codigo": Venda.codigo, "valor": Venda.valor, "datavenda": Venda.datavenda, "clienteid": Venda.clienteid, "datacriacao": Venda.datacriacao, "datamodificacao": Venda.datamodificacao}     

    #SELECIONAR TUDO - ENDPOINT PRODUTO

@app.route("/produto",methods = ["GET"])
def seleciona_produto():
    produto_objetos = Produto.query.all()
    produto_json = [produto.to_json() for produto in produto_objetos]
    print(produto_json)
    
    return gera_response(200, "produto" , produto_json, "ok")

    #SELECIONAR TUDO - ENDPOINT ESTOQUE

@app.route("/estoque",methods = ["GET"])
def seleciona_estoque():
    estoque_objetos = Estoque.query.all()
    estoque_json = [estoque.to_json() for estoque in estoque_objetos]
    print(estoque_json)
    
    return gera_response(200, "estoque" , estoque_json, "ok")


     #SELECIONAR TUDO - ENDPOINT CLIENTE

@app.route("/cliente",methods = ["GET"])
def seleciona_cliente():
    cliente_objetos = Cliente.query.all()
    cliente_json = [cliente.to_json() for cliente in cliente_objetos]
    print(cliente_json)
    
    return gera_response(200, "cliente" , cliente_json, "ok")


    #SELECIONAR TUDO - ENDPOINT VENDA

@app.route("/venda", methods = ["GET"])
def seleciona_venda():
    venda_objetos = Venda.query.all()
    venda_json = [venda.to_json() for venda in venda_objetos]
    print(venda_json)
    
    return gera_response(200, "venda" , venda_json, "ok")


    #SELEÇÃO INDIVIDUAL - ENDPOINT PRODUTO

@app.route("/produto/<id>", methods = ["GET"])
def seleciona_produtos(id):
    produto_objeto = Produto.query.filter_by(id = id).first()
    produto_json = produto_objeto.to_json()

    return gera_response(200, "produto" , produto_json)


    #SELEÇÃO INDIVIDUAL - ENDPOINT ESTOQUE

@app.route("/estoque/<id>", methods = ["GET"])
def seleciona_estoques(id):
    estoque_objeto = Estoque.query.filter_by(id = id).first()
    estoque_json = estoque_objeto.to_json()

    return gera_response(200, "estoque" , estoque_json)


    #SELEÇÃO INDIVIDUAL - ENDPOINT CLIENTE

@app.route("/cliente/<id>", methods = ["GET"])
def seleciona_clientes(id):
    cliente_objeto = Cliente.query.filter_by(id = id).first()
    cliente_json = cliente_objeto.to_json()

    return gera_response(200, "cliente" , cliente_json)


    #SELEÇÃO INDIVIDUAL - ENDPOINT VENDA 

@app.route("/venda/<id>", methods = ["GET"])
def seleciona_vendas(id):
    venda_objeto = Venda.query.filter_by(id = id).first()
    venda_json = venda_objeto.to_json()

    return gera_response(200, "venda" , venda_json)

     #CADASTRO  - ENDPOINT PRODUTO

@app.route("/produto", methods = ["POST"])
def cria_produto():
    body = request.get_json()

    try:
        produto = Produto(codigo = body["codigo"], nome = body["nome"], descricao = body["descricao"], categoriaid = body["categoriaid"], datacriacao = body["datacriacao"], datamodificacao = body["datamodificacao"],  )
        db.session.add(produto)
        db.session.commit()
        return gera_response(201, "produto", produto.to_json(), " Produto criado com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "produto", {}, "Erro ao cadastrar produto")

     #CADASTRO  - ENDPOINT ESTOQUE

@app.route("/estoque", methods = ["POST"])
def cria_estoque():
    body = request.get_json()

    try:
        estoque = Estoque(produtoid = body["produtoid"], quantidade = body["quantidade"], datacriacao = body["datacriacao"], datamodificacao = body["datamodificacao"])
        db.session.add(estoque)
        db.session.commit()
        return gera_response(201, "estoque", estoque.to_json(), "Estoque adicionado com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "estoque", {}, "Erro ao adicionar estoque")

    #CADASTRO  - ENDPOINT CATEGORIA

@app.route("/categoria", methods = ["POST"])
def cria_categoria():
    body = request.get_json()

    try:
        categoria = Categoria(codigo = body["codigo"], nome = body["nome"], datacriacao = body["datacriacao"], datamodificacao = body["datamodificacao"])
        db.session.add(categoria)
        db.session.commit()
        return gera_response(201, "categoria", categoria.to_json(), "Categoria adicionada com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "categoria", {}, "Erro ao adicionar categoria")

     #CADASTRO  - ENDPOINT CLIENTE

@app.route("/cliente", methods = ["POST"])
def cria_cliente():
    body = request.get_json()

    try:
        cliente = Cliente(codigo = body["codigo"], nome = body["nome"], datanascimento = body["datanascimento"], email = body["email"], datacriacao = body["datacriacao"], datamodificacao = body["datamodificacao"])
        db.session.add(cliente)
        db.session.commit()
        return gera_response(201, "cliente", cliente.to_json(), " Cliente criado com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "cliente", {}, "Erro ao cadastrar cliente")


    #CADASTRO  - ENDPOINT VENDA

@app.route("/venda", methods = ["POST"])
def cria_venda():
    body = request.get_json()

    try:
        venda = Venda(codigo = body["codigo"], valor = body["valor"], datavenda = body["datavenda"], clienteid = body["clienteid"], datacriacao = body["datacriacao"], datamodificacao = body["datamodificacao"])
        db.session.add(venda)
        db.session.commit()
        return gera_response(201, "venda", venda.to_json(), " Venda criada com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "venda", {}, "Erro ao cadastrar venda")

     #ATUALIZAR  - ENDPOINT PRODUTO

@app.route("/produto/<id>", methods = ["PUT"])
def atualiza_produto(id):
   # pegar produto
    produto_objeto = Produto.query.filter_by(id = id).first()
   # pegar modificacoes
    body = request.get_json()
    
    try:
        if('codigo' in body):
            produto_objeto.codigo = body['codigo']
        if('nome' in body):
            produto_objeto.nome = body['nome']
        if('descricao' in body):
            produto_objeto.descricao = body['descricao']
        if('categoriaid' in body):
            produto_objeto.categoriaid = body['categoriaid']
        if('datacriacao' in body):
            produto_objeto.datacriacao = body['datacriacao']
        if('datamodificacao' in body):
            produto_objeto.datamodificacao = body['datamodificacao']

        db.session.add(produto_objeto)
        db.session.commit()
        return gera_response(200, "produto", produto_objeto.to_json(), " Produto atualizado com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "produto", {}, "Erro ao atualizar o produto")

        #ATUALIZAR  - ENDPOINT ESTOQUE

@app.route("/estoque/<id>", methods = ["PUT"])
def atualiza_estoque(id):
    # pegar estoque
    estoque_objeto = Estoque.query.filter_by(id = id).first()
    # pegar modificacoes
    body = request.get_json()
    
    try:
        if('produtoid' in body):
            estoque_objeto.produtoid = body['produtoid']
        if('quantidade' in body):
            estoque_objeto.quantidade = body['quantidade']
        if('datacriacao' in body):
            estoque_objeto.datacriacao = body['datacriacao']
        if('datamodificacao' in body):
            estoque_objeto.datamodificacao = body['datamodificacao']
        
        db.session.add(estoque_objeto)
        db.session.commit()
        return gera_response(200, "estoque", estoque_objeto.to_json(), " Estoque atualizado com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "estoque", {}, "Erro ao atualizar o estoque")


        #ATUALIZAR  - ENDPOINT CATEGORIA

@app.route("/categoria/<id>", methods = ["PUT"])
def atualiza_categoria(id):
    # pegar infos de categoria
    categoria_objeto = Categoria.query.filter_by(id = id).first()
    # pegar modificacoes
    body = request.get_json()
    
    try:
        if('codigo' in body):
            categoria_objeto.codigo = body['codigo']
        if('nome' in body):
            categoria_objeto.nome = body['nome']
        if('datacriacao' in body):
           categoria_objeto.datacriacao = body['datacriacao']
        if('datamodificacao' in body):
           categoria_objeto.datamodificacao = body['datamodificacao']
        
        db.session.add(categoria_objeto)
        db.session.commit()
        return gera_response(200, "categoria", categoria_objeto.to_json(), " Categoria atualizado com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "categoria", {}, "Erro ao atualizar a categoria")


        #ATUALIZAR  - ENDPOINT CLIENTE

@app.route("/cliente/<id>", methods = ["PUT"])
def atualiza_cliente(id):
    # pegar infos do cliente
    cliente_objeto = Cliente.query.filter_by(id = id).first()
    # pegar modificacoes
    body = request.get_json()
    
    try:
        if('codigo' in body):
            cliente_objeto.codigo = body['codigo']
        if('nome' in body):
            cliente_objeto.nome = body['nome']
        if('datanascimento' in body):
            cliente_objeto.datanascimento = body['datanascimento']
        if('email' in body):
            cliente_objeto.email = body['email']
        if('datacriacao' in body):
            cliente_objeto.datacriacao = body['datacriacao']
        if('datamodificacao' in body):
            cliente_objeto.datamodificacao = body['datamodificacao']
        
        db.session.add(cliente_objeto)
        db.session.commit()
        return gera_response(200, "cliente", cliente_objeto.to_json(), " Cliente atualizado com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "cliente", {}, "Erro ao atualizar as informações do cliente")


        #ATUALIZAR  - ENDPOINT VENDA

@app.route("/venda/<id>", methods = ["PUT"])
def atualiza_venda(id):
    # pegar infos referente a venda
    venda_objeto = Venda.query.filter_by(id = id).first()
    # pegar modificacoes
    body = request.get_json()
    
    try:
        if('codigo' in body):
            venda_objeto.codigo = body['codigo']
        if('valor' in body):
            venda_objeto.valor = body['valor']
        if('datavenda' in body):
            venda_objeto.datavenda = body['datavenda']
        if('clienteid' in body):
            venda_objeto.clienteid = body['clienteid']
        if('datacriacao' in body):
            venda_objeto.datacriacao = body['datacriacao']
        if('datamodificacao' in body):
            venda_objeto.datamodificacao = body['datamodificacao']
        
        db.session.add(venda_objeto)
        db.session.commit()
        return gera_response(200, "venda", venda_objeto.to_json(), " Informações da venda atualizadas com Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "venda", {}, "Erro ao atualizar as informações de venda")

    #DELETAR  - ENDPOINT PRODUTO

@app.route("/produto/<id>", methods = ["DELETE"])
def deleta_produto(id):
    produto_objeto = Produto.query.filter_by(id = id).first()
    
    try:
        db.session.delete(produto_objeto)
        db.session.commit()
        return gera_response(200, "produto", produto_objeto.to_json(), "Produto deletado com Sucesso")
    except Exception as e:
        print('Erro',e)
        return gera_response(400, "produto", {}, "Erro ao deletar produto")


    # FUNÇÃO INFORME STATUS

def gera_response(status, nome_do_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem
    
    return Response(json.dumps(body), status = status,  mimetype = "application/json")


app.run()