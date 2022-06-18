from cmath import e
from pprintpp import pprint as pp
from db.database import Graph
from helper.write_a_json import write_a_json


class Pessoa(object):
    def __init__(self):
        self.db = Graph(uri='bolt://3.82.202.75:7687',
                        user='neo4j', password='leakages-men-request')

    def create(self, person):
        return self.db.execute_query('CREATE (n:Pessoa {nome:$nome, idade:$idade, sexo:$sexo, nacionalidade:$nacionalidade}) return n',
                                     {'nome': person['nome'], 'idade': person['idade'], 'sexo': person['sexo'], 'nacionalidade': person['nacionalidade']})

    def read_by_name(self, person):
        return self.db.execute_query('MATCH (n:Pessoa {nome:$nome}) RETURN n',
                                     {'nome': person['nome']})
    
    def update_age(self, person):
        return self.db.execute_query('MATCH (n:Pessoa {nome:$nome}) SET n.idade = $idade RETURN n',
                                     {'nome': person['nome'], 'idade': person['idade']})

    def delete(self, person):
        return self.db.execute_query('MATCH (n:Pessoa {nome:$nome}) DETACH DELETE n',
                                     {'nome': person['nome']})

    def create_relation(self, person, producao, nota, favorito):
        return self.db.execute_query('MATCH (n:Pessoa {nome:$nome1}), (m:Producao {nome:$nome2}) CREATE (n)-[r:ASSISTIU{nota:$nota, favorito:$favorito}]->(m) RETURN n, r, m',
                                     {'nome1': person['nome'], 'nome2': producao['nome'], 'nota': nota, 'favorito': favorito})

class Producao(object):
    def __init__(self):
        self.db = Graph(uri='bolt://3.82.202.75:7687',
                        user='neo4j', password='leakages-men-request')

    def create(self, producao):
        return self.db.execute_query('CREATE (n:Producao {nome:$nome, tipo:$tipo, genero:$genero, lancamento:$lancamento, episodios:$episodios}) return n',
                                     {'nome': producao['nome'], 'tipo': producao['tipo'], 'genero': producao['genero'], 'lancamento': producao['lancamento'], 'episodios': producao['episodios']})

    def read_by_name(self, producao):
        return self.db.execute_query('MATCH (n:Producao {nome:$nome}) RETURN n',
                                     {'nome': producao['nome']})
    
    def update_episodios(self, producao):
        return self.db.execute_query('MATCH (n:Producao {nome:$nome}) SET n.episodios = $episodios RETURN n',
                                     {'nome': producao['nome'], 'episodios': producao['episodios']})

    def delete(self, producao):
        return self.db.execute_query('MATCH (n:Producao {nome:$nome}) DETACH DELETE n',
                                     {'nome': producao['nome']})


def divider():
    print('\n' + '-' * 80 + '\n')

print("Selecione qual deseja adicionar:")
option1 = input('1. User\n2. Produção\n')

if option1 == '1':
    dao = Pessoa()
    while 1:    
        option = input('1. Create\n2. Read\n3. Update\n4. Delete\n5. Avaliação\n')

        if option == '1':
            nome = input('  Nome: ')
            idade = input('  Idade: ')
            sexo = input('  Sexo: ')
            nacionalidade = input('  Nacionalidade: ')
            pessoa = {
                'nome': nome,
                'idade': idade,
                'sexo': sexo,
                'nacionalidade': nacionalidade
            }
            aux = dao.create(pessoa)
            divider()

        elif option == '2':
            nome = input('  Nome: ')
            pessoa = {
                'nome': nome
            }
            aux = dao.read_by_name(pessoa)
            write_a_json(aux,"out")
            pp(aux)
            divider()

        elif option == '3':
            nome = input('  Nome: ')
            idade = input('  Idade: ')
            pessoa = {
                'nome': nome,
                'idade': idade
            }
            aux = dao.update_age(pessoa)
            divider()

        elif option == '4':
            nome = input('  Nome: ')
            pessoa = {
                'nome': nome
            }
            aux = dao.delete(pessoa)
            divider()

        elif option == '5':
            nome = input('  Nome: ')
            pessoa = {
                'nome': nome
            }
            title = input('  Titulo: ')
            producao = {
                'nome': title
            }
            nota = input('  Nota: ')
            favorito = input('  Favorito: ')
            aux = dao.create_relation(pessoa,producao,nota,favorito)
            divider()

        else:
            break
elif option1 == '2':
    dao = Producao()
    while 1:    
        option = input('1. Create\n2. Read\n3. Update\n4. Delete\n')

        if option == '1':
            nome = input('  Nome: ')
            tipo = input('  Tipo: ')
            genero = input('  Genero: ')
            lancamento = input('  Lançamento: ')
            episodios = input('  Episódios: ')
            producao = {
                'nome': nome,
                'tipo': tipo,
                'genero': genero,
                'lancamento': lancamento,
                'episodios': episodios
            }
            aux = dao.create(producao)
            divider()

        elif option == '2':
            nome = input('  Nome: ')
            producao = {
                'nome': nome
            }
            aux = dao.read_by_name(producao)
            pp(aux)
            divider()

        elif option == '3':
            nome = input('  Nome: ')
            episodios = input('  Episódios: ')
            producao = {
                'nome': nome,
                'episodios': episodios
            }
            aux = dao.update_age(producao)
            divider()

        elif option == '4':
            nome = input('  Nome: ')
            producao = {
                'nome': nome
            }
            aux = dao.delete(producao)
            divider()

        else:
            break


dao.db.close()