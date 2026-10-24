import model
from banco import iniciar
from servidor import executar

def pagina(termo, mensagem):
    from view import renderizar
    return renderizar(model.listar(termo), model.reservas(), termo, mensagem)

def acao(rota, id):
    if rota == '/reservar':
        model.reservar(id)
        return 'Reserva criada por 24 horas!'
    if rota == '/cancelar':
        model.cancelar(id)
        return 'Reserva cancelada.'
    raise ValueError('Ação desconhecida.')

if __name__ == '__main__':
    iniciar()
    executar()
