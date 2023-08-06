"""
This module defines two decorators, based on the code from
http://forrst.com/posts/Yet_another_caching_property_decorator_for_Pytho-PBy

They are both designed to cache class properties, but have the added
functionality of being automatically updated when a parent property is
updated.
"""
from functools import update_wrapper

def hidden_loc(obj,name):
    """
    Generate the location of a hidden attribute.
    Importantly deals with attributes beginning with an underscore.
    """
    return ("_" + obj.__class__.__name__ + "__"+ name).replace("___", "__")

def cached_property(*parents):
    """
    A robust property caching decorator.

    This decorator only works when used with the entire system here....

    Usage::
       class CachedClass(Cache):


           @cached_property("parent_parameter")
           def amethod(self):
              ...calculations...
              return final_value

           @cached_property("amethod")
           def a_child_method(self): #method dependent on amethod
              final_value = 3*self.amethod
              return final_value

    This code will calculate ``amethod`` on the first call, but return the cached
    value on all subsequent calls. If any parent parameter is modified, the
    calculation will be re-performed.
    """

    def cache(f):
        name = f.__name__

        def _get_property(self):
            # Location of the property to be accessed
            prop = hidden_loc(self,name)

            # Locations of indexes
            recalc = hidden_loc(self,"recalc")
            recalc_prpa = hidden_loc(self,"recalc_prop_par")
            recalc_papr = hidden_loc(self,"recalc_par_prop")

            # If recalc is constructed, and it needs to be updated,
            # or if recalc is NOT constructed, recalculate
            if getattr(self, recalc).get(name, True):
                value = f(self)
                setattr(self, prop, value)

            # If recalc constructed and doesn't need updating, just return.
            else:
                return  getattr(self, prop)

            # Figure out if it is a sub-class method
            # To be sub-class, it must already be in the recalc dict, but some
            # of the parents (if parameters) won't be in the papr dict, and also
            # if some parents are properties, THEIR parents won't be in prpa.
            # FIXME: this must be relatively slow, must be a better way.
            is_sub = False
            not_in_papr = any(p not in getattr(self, recalc_papr) for p in parents)
            if not_in_papr and name in getattr(self, recalc):
                all_pars = []
                if any(p in getattr(self, recalc_prpa) for p in parents):
                    for p in parents:
                        all_pars += list(getattr(self, recalc_prpa).get(p, []))
                if any(p not in getattr(self, recalc_prpa)[name] for p in all_pars):
                    is_sub = True


            # At this point, the value has been calculated.
            # If this quantity isn't in recalc, we need to construct an entry for it.
            if name not in getattr(self, recalc) or is_sub:
                final = set()
                # For each of its parents, either get all its already known parameters,
                # or just add the parent to a list (in this case it's a parameter itself).
                for p in parents:
                    # Hit each parent to make sure it's evaluated
                    getattr(self, p)
                    if p in getattr(self, recalc_prpa):
                        final |= set(getattr(self, recalc_prpa)[p])
                    else:
                        final.add(p)

                # final is a set of pure parameters that affect this quantity
                if name in getattr(self, recalc_prpa):
                    # This happens in the case of inheritance
                    getattr(self, recalc_prpa)[name] |= final
                else:
                    getattr(self, recalc_prpa)[name] = final

                # Go through each parameter and add the current quantity to its
                # entry (inverse of prpa).
                for e in final:
                    if e in getattr(self, recalc_papr):
                        getattr(self, recalc_papr)[e].add(name)
                    else:
                        getattr(self, recalc_papr)[e] = set([name])

            getattr(self, recalc)[name] = False
            return value
        update_wrapper(_get_property, f)

        def _del_property(self):
            # Locations of indexes
            recalc = hidden_loc(self,"recalc")
            recalc_prpa = hidden_loc(self,"recalc_prop_par")
            recalc_papr = hidden_loc(self,"recalc_par_prop")

            # Delete the property AND its recalc dicts
            try:
                prop = hidden_loc(self,name)
                delattr(self, prop)
                del getattr(self, recalc)[name]
                del getattr(self, recalc_prpa)[name]
                for e in getattr(self, recalc_papr):
                    if name in getattr(self, recalc_papr)[e]:
                        getattr(self, recalc_papr)[e].remove(name)
            except AttributeError:
                pass

        return property(_get_property, None, _del_property)
    return cache

def obj_eq(ob1, ob2):
    try:
        if ob1 == ob2:
            return True
        else:
            return False
    except ValueError:
        if  (ob1 == ob2).all():
            return True
        else:
            return False


def parameter(f):
    """
    A simple cached property which acts more like an input value.

    This cached property is intended to be used on values that are passed in
    ``__init__``, and can possibly be reset later. It provides the opportunity
    for complex setters, and also the ability to update dependent properties
    whenever the value is modified.

    Usage::
       @set_property("amethod")
       def parameter(self,val):
           if isinstance(int,val):
              return val
           else:
              raise ValueError("parameter must be an integer")

       @cached_property()
       def amethod(self):
          return 3*self.parameter

    Note that the definition of the setter merely returns the value to be set,
    it doesn't set it to any particular instance attribute. The decorator
    automatically sets ``self.__parameter = val`` and defines the get method
    accordingly
    """

    name = f.__name__
    par_ext = "__parameters"

    def _set_property(self, val):
        prop = hidden_loc(self, name)

        # The following does any complex setting that is written into the code
        val = f(self, val)

        # Locations of indexes
        recalc = hidden_loc(self, "recalc")
        recalc_prpa = hidden_loc(self, "recalc_prop_par")
        recalc_papr = hidden_loc(self, "recalc_par_prop")
        parameters = hidden_loc(self,"parameters")

        try:
            # If the property has already been set, we can grab its old value
#            old_val = getattr(self, prop)
            old_val = self._get_property()
            doset = False
        except AttributeError:
            # Otherwise, it has no old value.
            old_val = None
            doset = True

            # It's not been set before, so add it to our list of parameters
            try:
                # Only works if something has been set before
                parlist =  getattr(self,parameters)
                parlist += [name]
                setattr(self,parameters,parlist)
            except AttributeError:
                # If nothing has ever been set, start a list
                setattr(self, parameters, [name])

                # Given that *at least one* parameter must be set before properties are calculated,
                # we can define the original empty indexes here.
                setattr(self, recalc, {})
                setattr(self, recalc_prpa, {})
                setattr(self, recalc_papr, {})

        # If either the new value is different from the old, or we never set it before
        if not obj_eq(val, old_val) or doset:
            # Then if its a dict, we update it
            if isinstance(val, dict) and hasattr(self, prop) and val:
                getattr(self, prop).update(val)
            # Otherwise, just overwrite it. Note if dict is passed empty, it clears the whole dict.
            else:
                setattr(self, prop, val)

            # Make sure children are updated
            for pr in getattr(self, recalc_papr).get(name, []):
                getattr(self, recalc)[pr] = True

    update_wrapper(_set_property, f)

    def _get_property(self):
        prop = hidden_loc(self,name)
        return getattr(self, prop)

    # Here we set the documentation
    doc = (f.__doc__ or "").strip()
    if doc.startswith("\n"):
        doc = doc[1:]

    return  property(_get_property, _set_property, None,"**Parameter**: "+doc)#