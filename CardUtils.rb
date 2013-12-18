# This class extension adds the ability to convert a string into a Playing Card.
# the string should be of the form:
#          <rank><delimiter><suit>
# where <rank> :== a number from 2-10, J, Q, K, or A
#       <delimiter> :== "" or "of" or "-"
#       <suit> :== H S D C
# case of the characters is not significant
#
# requires the PlayingCard class.
class String
  def to_card
    # the RE splits sequences similar to: 5S 5-S 10-C 10C, etc.
    if rank_suit=/\s*(10|[2-9]|[JQKA])\W*[of]*\W*([CHSD])\w*/i.match(self)
      PlayingCard.new(rank_suit[1], rank_suit[2])
    end
  end
end
    
