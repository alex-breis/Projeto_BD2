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

    # def read_relation(self, person1, person2):
    #     return self.db.execute_query('MATCH (n:Person {name:$name1})-[r]->(m:Person {name:$name2}) RETURN n, r, m',
    #                                  {'name1': person1['name'], 'name2': person2['name']})

def divider():
    print('\n' + '-' * 80 + '\n')

dao = Pessoa()

while 1:    
    option = input('1. Create\n2. Read\n3. Update\n4. Delete\n5. Relação\n')

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


dao.db.close()