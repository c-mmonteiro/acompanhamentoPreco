import MetaTrader5 as mt5
import time

class Acompanhamento:
    def __init__(self, opcao_vendida, quantidade_vendida, premio_vendido, opcao_comprada, quantidade_comprada, premio_comprada):

        mt5.initialize()


        # Pegar o valor de venda mais baixo da opção que se deseja comprar
        if mt5.market_book_add(opcao_vendida):
            time.sleep(1)
            val1 = mt5.market_book_get(opcao_vendida)
            if not val1:
                print(f'ALERTA: Problema na aquisição do valor de COMPRA ou de VENDA do ativo {opcao_vendida}')
            else:
                valor_compra = 100
                for idx, v in enumerate(val1):
                    if v.type == 1:
                        if valor_compra > v.price:
                            idx_compra = idx
                            valor_compra = v.price
                valor_comprar = val1[idx_compra].price

                valor_venda = 0
                for idx, v in enumerate(val1):
                    if v.type == 1:
                        if valor_venda < v.price:
                            idx_compra = idx
                            valor_venda = v.price
                valor_comprar_medio = (valor_compra + valor_venda)/2                
        else:
            print(f'ALERTA: O ativo {opcao_vendida} não pode ser adicionado!')

        mt5.market_book_release(opcao_vendida)

        # Pegar o valor de compra mais alto da opção que se deseja vender
        if mt5.market_book_add(opcao_comprada):
            time.sleep(1)
            val1 = mt5.market_book_get(opcao_comprada)
            if not val1:
                print(f'ALERTA: Problema na aquisição do valor de COMPRA ou de VENDA do ativo {opcao_comprada}')
            else:
                valor_venda = 0
                for idx, v in enumerate(val1):
                    if v.type == 2:
                        if valor_venda < v.price:
                            idx_compra = idx
                            valor_venda = v.price
                valor_vender = val1[idx_compra].price

                valor_compra = 100
                for idx, v in enumerate(val1):
                    if v.type == 1:
                        if valor_compra > v.price:
                            idx_compra = idx
                            valor_compra = v.price

                valor_vender_medio = (valor_compra + valor_venda)/2                  
        else:
            print(f'ALERTA: O ativo {opcao_comprada} não pode ser adicionado!')

        mt5.market_book_release(opcao_comprada)

        mt5.shutdown()

        diferenca = valor_comprar - valor_vender

        posicao = quantidade_comprada*(valor_vender - premio_comprada) + quantidade_vendida*(premio_vendido - valor_comprar)

        posicao_medio = quantidade_comprada*(valor_vender_medio - premio_comprada) + quantidade_vendida*(premio_vendido - valor_comprar_medio)

        print(f'A preço de book: {posicao} /// Ao valor médio do book {posicao_medio}')

        
while 1:

    Acompanhamento('BOVAW12', 500, 9.80, 'BOVAW109', 1000, 2.96)
    time.sleep(10)
