from .baseresource import BaseResource


class EventType(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'event_type'
        attributes = {
            'id': 'id',
            'name': 'name'
        }


class EventTypeResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'event_type_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'eventType': EventType
        }


class Competition(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'competition'
        attributes = {
            'id': 'id',
            'name': 'name'
        }


class CompetitionResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'competition_result'
        attributes = {
            'marketCount': 'market_count',
            'competitionRegion': 'competition_region'
        }
        sub_resources = {
            'competition': Competition
        }


class TimeRange(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'time_range'
        attributes = {
            'from': '_from',
            'to': 'to'
        }
        datetime_attributes = (
            'from',
            'to'
        )


class TimeRangeResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'time_range_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'timeRange': TimeRange
        }


class Event(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'event'
        attributes = {
            'id': 'id',
            'openDate': 'open_date',
            'timezone': 'time_zone',
            'countryCode': 'country_code',
            'name': 'name',
            'venue': 'venue'
        }
        datetime_attributes = (
            'openDate'
        )


class EventResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'event_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'event': Event
        }


class MarketTypeResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'market_type_result'
        attributes = {
            'marketCount': 'market_count',
            'marketType': 'market_type'
        }


class CountryResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'country_result'
        attributes = {
            'marketCount': 'market_count',
            'countryCode': 'country_code'
        }


class VenueResult(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'venue_result'
        attributes = {
            'marketCount': 'market_count',
            'venue': 'venue'
        }


class MarketCatalogueDescription(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'description'
        attributes = {
            'bettingType': 'betting_type',
            'bspMarket': 'bsp_market',
            'discountAllowed': 'discount_allowed',
            'marketBaseRate': 'market_base_rate',
            'marketTime': 'market_time',
            'marketType': 'market_type',
            'persistenceEnabled': 'persistence_enabled',
            'regulator': 'regulator',
            'rules': 'rules',
            'rulesHasDate': 'rules_has_date',
            'suspendTime': 'suspend_time',
            'turnInPlayEnabled': 'turn_in_play_enabled',
            'wallet': 'wallet',
            'eachWayDivisor': 'each_way_divisor',
            'clarifications': 'clarifications'
        }
        datetime_attributes = (
            'marketTime',
            'suspendTime'
        )


class RunnerCatalogue(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'selectionId': 'selection_id',
            'runnerName': 'runner_name',
            'sortPriority': 'sort_priority',
            'handicap': 'handicap',
            'metadata': 'metadata'
        }


class MarketCatalogue(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'market_catalogue'
        attributes = {
            'marketId': 'market_id',
            'marketName': 'market_name',
            'totalMatched': 'total_matched',
            'marketStartTime': 'market_start_time'
        }
        sub_resources = {
            'competition': Competition,
            'event': Event,
            'eventType': EventType,
            'description': MarketCatalogueDescription,
            'runners': RunnerCatalogue
        }
        datetime_attributes = (
            'marketStartTime'
        )


class RunnerBookSP(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'sp'
        attributes = {
            'nearPrice': 'near_price',
            'farPrice': 'far_price',
            'backStakeTaken': 'back_stake_taken',
            'layLiabilityTaken': 'lay_liability_taken',
            'actualSP': 'actual_sp'
        }


class RunnerBookEX(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'ex'
        attributes = {
            'availableToBack': 'available_to_back',
            'availableToLay': 'available_to_lay',
            'tradedVolume': 'traded_volume'
        }


class RunnerBookOrder(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'orders'
        attributes = {
            'betId': 'bet_id',
            'avgPriceMatched': 'avg_price_matched',
            'bspLiability': 'bsp_liability',
            'orderType': 'order_type',
            'persistenceType': 'persistence_type',
            'placedDate': 'placed_date',
            'price': 'price',
            'side': 'side',
            'size': 'size',
            'sizeCancelled': 'size_cancelled',
            'sizeLapsed': 'size_lapsed',
            'sizeMatched': 'size_matched',
            'sizeRemaining': 'size_remaining',
            'sizeVoided': 'size_voided',
            'status': 'status'
        }
        datetime_attributes = (
            'placedDate'
        )


class RunnerBookMatch(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'matches'
        attributes = {
            'betId': 'bet_id',
            'matchId': 'match_id',
            'price': 'price',
            'side': 'side',
            'size': 'size',
            'matchDate': 'match_date'
        }
        datetime_attributes = (
            'matchDate'
        )


class RunnerBook(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'selectionId': 'selection_id',
            'status': 'status',
            'totalMatched': 'total_matched',
            'adjustmentFactor': 'adjustment_factor',
            'handicap': 'handicap',
            'lastPriceTraded': 'last_price_traded',
            'removalDate': 'removal_date',
        }
        sub_resources = {
            'sp': RunnerBookSP,
            'ex': RunnerBookEX,
            'orders': RunnerBookOrder,
            'matches': RunnerBookMatch
        }
        datetime_attributes = (
            'removalDate',
        )


class MarketBook(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'market_book'
        attributes = {
            'marketId': 'market_id',
            'betDelay': 'bet_delay',
            'bspReconciled': 'bsp_reconciled',
            'complete': 'complete',
            'crossMatching': 'cross_matching',
            'inplay': 'inplay',
            'isMarketDataDelayed': 'is_market_data_delayed',
            'lastMatchTime': 'last_match_time',
            'numberOfActiveRunners': 'number_of_active_runners',
            'numberOfRunners': 'number_of_runners',
            'numberOfWinners': 'number_of_winners',
            'runnersVoidable': 'runners_voidable',
            'status': 'status',
            'totalAvailable': 'total_available',
            'totalMatched': 'total_matched',
            'version': 'version',
        }
        sub_resources = {
            'runners': RunnerBook
        }
        datetime_attributes = (
            'lastMatchTime',
        )


class PriceSize(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'price_size'
        attributes = {
            'price': 'price',
            'size': 'size'
        }


class CurrentOrder(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'orders'
        attributes = {
            'betId': 'bet_id',
            'averagePriceMatched': 'average_price_matched',
            'bspLiability': 'bsp_liability',
            'handicap': 'handicap',
            'marketId': 'market_id',
            'matchedDate': 'matched_date',
            'orderType': 'order_type',
            'persistenceType': 'persistence_type',
            'placedDate': 'placed_date',
            'regulatorCode': 'regulator_code',
            'selectionId': 'selection_id',
            'side': 'side',
            'sizeCancelled': 'size_cancelled',
            'sizeLapsed': 'size_lapsed',
            'sizeMatched': 'size_matched',
            'sizeRemaining': 'size_remaining',
            'sizeVoided': 'size_voided',
            'status': 'status',
            'customerStrategyRef': 'customer_strategy_ref',
            'customerOrderRef': 'customer_order_ref'
        }
        sub_resources = {
            'priceSize': PriceSize
        }
        datetime_attributes = (
            'placedDate',
            'matchedDate'
        )


class CurrentOrders(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'current_orders'
        attributes = {
            'moreAvailable': 'more_available'
        }
        sub_resources = {
            'currentOrders': CurrentOrder
        }


class ClearedOrder(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'orders'
        attributes = {
            'betId': 'bet_id',
            'betCount': 'bet_count',
            'betOutcome': 'bet_outcome',
            'eventId': 'event_id',
            'eventTypeId': 'event_type_id',
            'handicap': 'handicap',
            'lastMatchedDate': 'last_matched_date',
            'marketId': 'market_id',
            'orderType': 'order_type',
            'persistenceType': 'persistence_type',
            'placedDate': 'placed_date',
            'priceMatched': 'price_matched',
            'priceReduced': 'price_reduced',
            'priceRequested': 'price_requested',
            'profit': 'profit',
            'selectionId': 'selection_id',
            'settledDate': 'settled_date',
            'side': 'side',
            'sizeSettled': 'size_settled',
            'customerStrategyRef': 'customer_strategy_ref',
            'customerOrderRef': 'customer_order_ref'
        }
        datetime_attributes = (
            'placedDate',
            'lastMatchedDate',
            'settledDate'
        )


class ClearedOrders(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'cleared_orders'
        attributes = {
            'moreAvailable': 'more_available'
        }
        sub_resources = {
            'clearedOrders': ClearedOrder
        }


class ProfitAndLosses(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'profit_and_losses'
        attributes = {
            'selectionId': 'selection_id',
            'ifWin': 'if_win',
            'ifLose': 'if_lose',
            'ifPlace': 'if_place'
        }


class MarketProfitLoss(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'market_profit_loss'
        attributes = {
            'marketId': 'market_id',
            'commissionApplied': 'commission_applied'
        }
        sub_resources = {
            'profitAndLosses': ProfitAndLosses
        }


class LimitOrder(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'order'
        attributes = {
            'persistenceType': 'persistence_type',
            'price': 'price',
            'size': 'size',
            'timeInForce': 'time_in_force',
            'minFillSize': 'min_fill_size',
            'betTargetType': 'bet_target_type',
            'betTargetSize': 'bet_target_size'
        }


class PlaceOrderInstruction(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'instruction'
        attributes = {
            'selectionId': 'selection_id',
            'side': 'side',
            'orderType': 'order_type',
            'handicap': 'handicap',
            'customerOrderRef': 'customer_order_ref'
        }
        sub_resources = {
            'limitOrder': LimitOrder
        }


class PlaceOrderInstructionReports(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'place_instruction_reports'
        attributes = {
            'status': 'status',
            'orderStatus': 'order_status',
            'betId': 'bet_id',
            'averagePriceMatched': 'average_price_matched',
            'sizeMatched': 'size_matched',
            'placedDate': 'placed_date',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'instruction': PlaceOrderInstruction
        }
        datetime_attributes = (
            'placedDate'
        )


class PlaceOrders(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'place_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': PlaceOrderInstructionReports
        }


class CancelOrderInstruction(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'instruction'
        attributes = {
            'betId': 'bet_id',
            'sizeReduction': 'size_reduction'
        }


class CancelOrderInstructionReports(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'cancel_instruction_reports'
        attributes = {
            'status': 'status',
            'sizeCancelled': 'size_cancelled',
            'cancelledDate': 'cancelled_date',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'instruction': CancelOrderInstruction
        }
        datetime_attributes = (
            'cancelledDate'
        )


class CancelOrders(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'cancel_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': CancelOrderInstructionReports
        }


class UpdateOrderInstruction(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'instruction'
        attributes = {
            'betId': 'bet_id',
            'newPersistenceType': 'new_persistence_type'
        }


class UpdateOrderInstructionReports(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'update_instruction_reports'
        attributes = {
            'status': 'status',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'instruction': UpdateOrderInstruction
        }


class UpdateOrders(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'update_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': UpdateOrderInstructionReports
        }


class ReplaceOrderInstructionReports(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'replace_instruction_reports'
        attributes = {
            'status': 'status',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'cancelInstructionReport': CancelOrderInstructionReports,
            'placeInstructionReport': PlaceOrderInstructionReports
        }


class ReplaceOrders(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'replace_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': ReplaceOrderInstructionReports
        }
