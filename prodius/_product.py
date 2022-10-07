'''
source: url - https://github.com/sekgobela-kevin/prodius
        commit Hash - de476e23a5447b2eb7af8000637b449aab200f55

Author: Sekgobela Kevin
Date: October 2022
Languages: Python 3
'''
from prodius import exceptions

try:
    from collections.abc import Iterable
except AttributeError:
    from collections import Iterable


class Product():
    def __init__(self, *iterables, repeat=1) -> None:
        self._iterables = iterables
        self._repeat = repeat

    @classmethod
    def to_iterators(cls, callables):
        # Returns list of iterables from iterable of callables
        return [iter(callable_()) for callable_ in callables]

    @classmethod
    def to_callable(cls, iterable, index=None):
        # Creates callable_ from iterable if not already callable_.
        if callable(iterable):
            return iterable
        else:
            if index!=0 and isinstance(iterable, Iterable):
                iterable = tuple(iterable)
            return lambda: iterable

    @classmethod
    def to_callables(cls, iterables):
        length = len(iterables)
        return [cls.to_callable(iterables[i], i) for i in range(length)]

    @classmethod
    def split_iterator(cls, iterator, split_size):
        # Split iterator into smaller 2D iterator
        iterator_group = []
        for value in iterator:
            iterator_group.append(value)
            if len(iterator_group) == split_size:
                yield iterator_group.copy()
                iterator_group.clear()
        if iterator_group:
            yield iterator_group

    @classmethod
    def product_grouped_callables(cls, callables, group_size=2):
        # Returns product of grouped callables
        # Method is not used
        grouped_callables =  cls.split_iterator(callables, group_size)
        for callables in grouped_callables:
            if len(callables) == 2:
                product = cls.product_double_callables(*callables)
            elif len(callables) == 1:
                product = cls.product_single_callable(callables[0])
            else:
                err_msg = "Three(3) or less callables expected not {}"
                raise exceptions.LimitError(err_msg.format(len(callables)))
            yield product

    @classmethod
    def product_double_callables(cls, callable1, callable2):
        # Returns product of two iterators in callables
        for item in callable1():
            for item2 in callable2():
                yield (item, item2)

    @classmethod
    def product_single_callable(cls, callable_):
        # Returns product of iterator in callable_
        for item in callable_():
            yield (item,)

    @classmethod
    def flatten_callable_product(cls, callable_):
        # Returns product of callable_ and flatten the product.
        # callable_ argument may call other callables through recursion
        # until product is returned.
        for product_item in callable_():
            product_item_ = []
            # This is an attempt to flatten product_item tuple
            for sub_item in product_item:
                for sub_sub_item in sub_item:
                    product_item_.append(sub_sub_item)
            yield tuple(product_item_)

    @classmethod
    def product_three_callables(cls, callables):
        if not len(callables) == 3:
            err_msg = "Three(3) iterables expected not {}"
            raise exceptions.LimitError(err_msg.format(len(callables)))
        last_two = callables[-2:]
        rest = callables[:-2]
        def final_callable_product():
            return cls.product_double_callables(*last_two)

        for callable_ in rest:
            previous_final_callable_product = final_callable_product

            def callable_product():
                return cls.product_single_callable(callable_)

            def final_callable_product():
                return cls.product_double_callables(callable_product, 
                previous_final_callable_product)
        return cls.flatten_callable_product(final_callable_product)


    @classmethod
    def product_four_callables(cls, callables):
        if not len(callables) == 4:
            err_msg = "Four(4) iterables expected not {}"
            raise exceptions.LimitError(err_msg.format(len(callables)))
        last_three_callables = callables[-3:]
        rest_callables = callables[:-3]

        def final_callable_product():
            return cls.product_three_callables(last_three_callables)

        for callable_ in rest_callables:
            previous_final_callable_product = final_callable_product

            def callable_product():
                return cls.product_single_callable(callable_)

            def final_callable_product():
                return cls.product_double_callables(callable_product, 
                previous_final_callable_product)
        return cls.flatten_callable_product(final_callable_product)
    

    @classmethod
    def product_callables_recursive(cls, callables):
        # Returns product of iterables in callables but limited
        # to 5 callables.
        if len(callables) == 0:
            return cls.product_single_callable(lambda :range(0))
        elif len(callables) == 1:
            return cls.product_single_callable(callables[0])
        elif len(callables) == 2:
            return cls.product_double_callables(*callables)
        elif len(callables) == 3:
            return cls.product_three_callables(callables)
        elif len(callables) == 4:
            return cls.product_four_callables(callables)
        else:
            err_msg = "{} iterables not supported(maximum is 4)"
            raise exceptions.LimitError(err_msg.format(len(callables)))

            
    @classmethod
    def product_callables_recursive_advanced(cls, callables):
        # Returns product of iterables in callables
        # This function raises recursion error on 12+ callables
        if len(callables) >= 12:
            err_msg = "{} iterables not supported(maximum is 11)"
            raise exceptions.LimitError(err_msg.format(len(callables)))

        if len(callables) <= 4:
            # Calculates product of 4 or less than iterables
            return cls.product_callables_recursive(callables)
        else:
            # Toatl Itarables that wont be part of group with 4 iterables
            total_leftout_callables = len(callables) % 4
            # Returns 2D iterator with 4 elements in each
            # It wont always be 4 elements on last group
            four_grouped_callables = list(cls.split_iterator(callables, 4))
            # Non zero if last group has elements less than four(4)
            if total_leftout_callables:
                # Gets group with less than 4 elements(callables)
                leftout_callables_group = four_grouped_callables[-1]
                # Gets the rest of callables groups
                rest_callables_groups = four_grouped_callables[:-1]
            else:
                # Theres no leftout callables
                leftout_callables_group = []
                rest_callables_groups = four_grouped_callables

            # Gets last four callables from rest_callables_groups
            last_four_callables_group = rest_callables_groups[-1]
            # Get rest of callables groups excluding last_four_callables_group
            rest_callables_groups = rest_callables_groups[:-1]

            def final_callable_product():
                # This function will be modified on each iteration.
                # Calculates product of callables in last_four_callables_group
                return cls.product_four_callables(last_four_callables_group)

            for callables_group in rest_callables_groups:
                # Store previous referance final_callable_product()
                previous_final_callable_product = final_callable_product

                # Create callable_ from product of callables_group
                def callable_product():
                    return cls.product_four_callables(callables_group)

                def merge_callable():
                    # Combine callable_product() with previous 
                    # final_callable_product()
                    return cls.product_double_callables(callable_product, 
                    previous_final_callable_product)

                # Modify final_callable_product() to include callable_product()
                def final_callable_product():
                    # Flatten result of merge_callable
                    return cls.flatten_callable_product(merge_callable)

            # Store previous referance final_callable_product()
            previous_final_callable_product_ = final_callable_product

            def final_callable_product():
                # This callable_ is for including leftout_callables
                # Checks if there were left out callables
                if leftout_callables_group:
                    # Creates callable_ for the left out callables
                    def leftout_callable():
                        return cls.product_callables_recursive(
                            leftout_callables_group
                        )
                    
                    def merge_callable():
                        # Combine final_callable_product() with leftout_callable()
                        # and return their product.
                        return cls.product_double_callables(
                                previous_final_callable_product_,
                                leftout_callable
                        )
                    # Flatten the product of combination of 
                    # final_callable_product() and leftout_callable()
                    return cls.flatten_callable_product(merge_callable)
                else:
                    return previous_final_callable_product_()     

            return final_callable_product()


    @classmethod
    def product_repeat_callables(cls, callables, repeat):
        # Yields products of callables in 'repeat' times
        for _ in range(repeat):
            def callable_func():
                return cls.product_callables_recursive_advanced(callables)
            yield callable_func
    
    @classmethod
    def product_callables_repeat(cls, callables, repeat):
        # Creates product of iterator in callables
        repeated_callables = list(cls.product_repeat_callables(
            callables, repeat=repeat
        ))        
        #print(list(repeated_callables)[0])
        def recursive_product_callable():
            # Recursion error expected on 12+ callables
            return cls.product_callables_recursive_advanced(repeated_callables)
        # Flattens each product removing unneccessay tuples
        return cls.flatten_callable_product(recursive_product_callable)

    @classmethod
    def product_callables(cls, callables, repeat=1):
        # Creates product of iterator in callables
        return cls.product_callables_repeat(callables, repeat=repeat)

    @classmethod
    def product(cls, *iterables, repeat=1):
        # Returns product of iterators similar to `itertools.product()`.
        # But iterables can contain callable_ objects like functions.
        iterables = cls.to_callables(iterables)
        return cls.product_callables(iterables, repeat=repeat)

    def __iter__(self):
        return iter(self.product(*self._iterables, repeat=self._repeat))


def product(*iterables, repeat=1):
    '''Returns cartesian product of iterators similar to `itertools.product()`.

    But also allows iterator to be a callable_ which should return the 
    iterator. Iterable does not always have to be a callable_ and function
    can be used just as builtin `itertools.product()`.
    
    Cartesian product is be calculated using recursion which brings risk of
    'RecursionError'. That causes number of iterables or repeat argument to
    be restricted to 12. Going beyond 12 would cause recursion error, this 
    is currently a bug to be fixed.'''
    return iter(Product(*iterables, repeat=repeat))


if __name__ == "__main__":
    def gen():
        for _ in range(3):
            yield _

    def range_callable(*arg, **kwags):
        return range(1,4000000000)

    def range_callable_2(*arg, **kwags):
        return range(4,700000000000)

    def range_callable_3(*arg, **kwags):
        return range(7,1000000000000000000000)

    #print(len(list(Product.product_callables_recursive_advanced([gen, gen, gen, gen]))))
    product_ = product(*[range(2)], repeat=11)

    count = 0
    for item in product_:
        if count == 1000000:
            break
        print(item)
        count+=1